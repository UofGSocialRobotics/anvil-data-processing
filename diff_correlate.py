from __future__ import division
import argparse
import sys
import math
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xmltodict
import json
from json import loads, dumps
from collections import OrderedDict, defaultdict



## Utils
flatten = lambda l: [item for sublist in l for item in sublist]

def prettyPrint(uglyJson):
    print(dumps(uglyJson, indent=4, sort_keys=True))

############ CUSTOM STUFF ############
######################################
## Lots of custom stuff to collapse ##
## tracks into one so that we can   ##
## compare multiple metaphors on    ##
## the same track. This is super    ##
## modulear though!                 ##
######################################

## Takes json that has dict for all the tracks you want to
## collapse, track name to collapse them into, and puts them all into one dict.
def collapse_tracks(json_struct, trackname, tracks_to_collapse):
    all_tracknames = json_struct.keys()

    dd = defaultdict(list)
    dics = []

    for track in tracks_to_collapse:
        all_tracknames.remove(track)
        dics.append(json_struct[track])

    for dic in dics:
        for key, val in dic.iteritems():  # .items() in Python 3.
            dd[key].append(val)

    # collapse into one item if necessary
    # start at 1, and this is how range works
    pop_me_later = len(dd.keys())
    for i in range(1, len(dd.keys())):
        for val in dd[str(i)]:
            dd["0"].append(val)

    # change the array of collapsed items into a dict
    # high key extremely proud of remembering this functional programming magic
    # NOTE be wary of all the elements being in the "0" item in dd
    zipped = dict(zip(map(str, range(0, len(dd["0"]))), dd["0"]))
    dd[trackname] = zipped

    # pop the extra tracks from the list conversion
    for extra_track_number in range(0, pop_me_later):
        dd.pop(str(extra_track_number))

    # add all the leftover elements that we didn't collapse
    for leftover_track in all_tracknames:
        dd[leftover_track] = json_struct[leftover_track]

    return dd


# THIS ASSUMES THE TRACKS ARE IN TIME ORDER (which is how
# they come out of the raw anvil file.)
# TODO could make this order-agnostic, but you dont have
# tons of time girl PRIORITIZE
# takes a JSON-ified annotation file and a list of track names
# to calculate correlations over
def get_all_intratrack_correlations(json_struct, trackNames, attr_to_diff):
    collapsed = collapse_tracks(json_struct, "Working", trackNames)
    instances = collapsed["Working"]
    num_instances = len(instances.keys())
    j = 1
    corr = []
    for i in range(0, num_instances):
        cur_elem = instances[str(i)]
        # go through the rest while there are diffs
        # checking for overlaps forwards
        # need to check for start and end time as numbers
        while (j < num_instances and overlaps(instances[str(j)], cur_elem)):
            # something can't be correlated with itself
            if cur_elem[attr_to_diff] != instances[str(j)][attr_to_diff]:
                corr.append([cur_elem[attr_to_diff], instances[str(j)][attr_to_diff]])
            # keep going
            j += 1
        # reset from next element. i will increment by 1 so we increment by 2
        j = i + 2

    return corr


## So need to get total instances of a particular metaphor
# given an annotation file and a set of track names to search over, searches
# for number of times attribute attr has value attr_val
def get_num_attribute_occurances(json_struct, trackNames, attr, attr_val):
    count = 0
    for trackName in trackNames:
        for instance in json_struct[trackName].keys():
            if(json_struct[trackName][instance][attr] == attr_val):
                count += 1
    return count


def list_of_lists_to_list_of_sets(list_of_lists):
    l = []
    for elem in list_of_lists:
        l.append(set(elem))
    return l


def dedupe_list_of_sets(L):
    return [set(item) for item in set(frozenset(item) for item in L)]

## I think I should define it as likelihood of 1 metaphor occuring given
## that another metaphor has occurred
## Correlation will not be symmetric!
## One metaphor can make another more likely, but not necessarily the
## other way around.
# where A and B are metaphors,
# Bayes: P(A|B) = (P(B|A)P(A)) / P(B)
# P(A) = num occurances of A / total occurances
# P(B) = num occurances of B / total occurances
# P (A & B) / P(A) + P(B)
# TODO explain "correlation" definition
def calc_correlation(json_struct, trackNames, attribute="Metaphor"):
    correlations = {}
    all_correlations = get_all_intratrack_correlations(json_struct, trackNames, attribute)
    # if there are NO correlations in these tracks
    if not all_correlations:
        return correlations
    # can change all of these to sets?
    all_correlations = list_of_lists_to_list_of_sets(all_correlations)
    for corr in all_correlations:
        # if something is "correlated" with itself (if an annotator overlaps
        # the same value on two separate tracks)
        if len(corr) < 2:
            continue
        for item in corr:
            # we're at individual metaphor level now
            # get number of correlations
            if item not in correlations.keys():
                correlations[item] = {}
            other_item = (corr - set([item])).pop()
            correlations[item][other_item] = all_correlations.count(corr) / get_num_attribute_occurances(json_struct, trackNames, attribute, item)

    return correlations



## so this deffo builds the json in a nice structure
def build_json(fileName):
    tree = ET.parse(fileName)
    json_structure = {}
    current_track = ""
    for elem in tree.iter():
        # relies on this being in order.
        if(elem.tag == "track"):
            current_track = elem.attrib["name"]
            json_structure[current_track] = {}
        elif(elem.tag == "el"):
            current_index = elem.attrib["index"]
            json_structure[current_track][current_index] = {}
            json_structure[current_track][current_index]["start"] = elem.attrib["start"]
            json_structure[current_track][current_index]["end"] = elem.attrib["end"]
        elif(elem.tag == "attribute"):
            json_structure[current_track][current_index][elem.attrib["name"]] = elem.text

    return(json_structure)

## check that the two jsons have the same general shape (dictionaries only)
## will not work if contains list of dicts and you want to typecheck those...
## too difficult and doesn't matter for this use case.
## NOTE this requires at least one annotation per track
def check_shape(json1, json2):
    dict_same = []
    if(set(json1.keys()) != set(json2.keys())):
        return False
    for key in json1.keys():
        if type(json1[key]) != type(json2[key]):
            return False
        # if it's a dict, check all the way down (provided both items)
        # have shapes to check
        if type(json1[key]) == dict:
            # both non-empty dicts
            if bool(json1[key]) and bool(json2[key]):
                # this would normally just be json1[key] and json2[key]
                # but because of the way the xml gets structures it turns
                # into a dictionary with more elements, not a list of dictionary.
                dict_same.append(check_shape(json1[key]["0"], json2[key]["0"]))
            # both empty dicts
            elif not bool(json1[key]) and not bool(json2[key]):
                dict_same.append(True)
            # one empty, one non-empty dict
            else:
                dict_same.append(False)

    return all(dict_same)

def overlaps(elem1, elem2):
    ## check that start and end time overlap in some way
    s1= float(elem1["start"])
    s2= float(elem2["start"])
    e1= float(elem1["end"])
    e2= float(elem2["end"])

    overlaps = False
    if (s1 >= s2 and e2 >= s1):
        overlaps = True
    elif (e1 >= s2 and e2 >= e1):
        overlaps = True
    elif (s1 >= s2 and e2 >= e1):
        overlaps = True
    elif (e1 >= e2 and s2 >= s1):
        overlaps = True

    return overlaps


# check for overlaps, basically
# if any item doesn't have an overlap, it's a difference
# at first, assume independence. I can change it so it searches over all metaphors later.
def compute_diffs_from_reference_track(reference_track, comparison_track, trackName, fn1, fn2, track_attributes_to_diff):
    track_diffs = []
    # makes this far easier to test, but lines 261-265 are not strictly necessary
    t_diffs = []
    if type(track_attributes_to_diff) == list:
        t_diffs = track_attributes_to_diff
    else:
        t_diffs = track_attributes_to_diff.keys()
    if trackName not in t_diffs:
        return []

    track_to_diff = track_attributes_to_diff[trackName]
    if "attributes" not in track_to_diff.keys():
        print "ERROR IN SPEC FILE, must supply track attributes to diff"
        return []

    attributes_to_diff = track_to_diff["attributes"]
    # nested for loop, not my finest work.
    for elem1 in reference_track:
        t1 = reference_track[elem1]
        found_diff = True       ## assume it's a difference until we find otherwise
        no_overlaps = True
        for elem2 in comparison_track:
            t2 = comparison_track[elem2]
            for attribute in attributes_to_diff:
                if overlaps(t1, t2):        # if we find something overlapping here, it could be the same!
                    no_overlaps = False     # at least we know for sure something is overlapping.
                    if t1[attribute] == t2[attribute]:
                        found_diff = False
        if found_diff:
            diff = {}
            if no_overlaps:
                diff = {
                    fn1: t1,
                    fn2: "No corresponding annotation found"
                }
            else:
                diff = {
                    fn1: t1,
                    fn2: t2
                }
            track_diffs.append(diff)

    return track_diffs



## hmm so right now this works but it's non-symmetric.
def compute_diffs_per_track(track1, track2, trackName, fn1, fn2, attributes):
    # at first, assume independence. I can change it so it searches over all metaphors later.
    track_diffs = {}
    track_diffs[trackName] = []
    track_diffs[trackName].append(compute_diffs_from_reference_track(track1, track2, trackName, fn1, fn2, attributes))
    track_diffs[trackName].append(compute_diffs_from_reference_track(track2, track1, trackName, fn2, fn1, attributes))
    track_diffs[trackName] = flatten(track_diffs[trackName])
    if not track_diffs[trackName]:
        # return None if empty list
        return

    # need to dedupe list of true conflicts
    # thanks SO: https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
    # use dict comparison, so only keep elements that are not in rest of initial list
    # -- only accessible through index n, hence use of enumerate
    track_diffs[trackName] = [i for n, i in enumerate(track_diffs[trackName]) if i not in track_diffs[trackName][n + 1:]]
    return track_diffs




#### TODO: implement cohen's kappa to calculate agreement if you have time

## Use cohen's kappa to calculate inter-annotator agreement on tracks we pay attention to.
## information can be found here: https://en.wikipedia.org/wiki/Cohen%27s_kappa
## "generally though tto be a more robust measure than simple percentage agreement calculation,
## as kappa takes into account the possibility of the agreement occurring by chance."
# def compute_inter_annotator_agreement_per_track(track1, track2, track_diffs):
#     p_o = # relative observed agreement among raters
#     p_e = # hypothetical probability of chance agreement
#     n = len(track1) # number of annotation instances
#     ## TODO make this a variable
#     k = 20 # number of options for annotation -- in this case 20 because 20 metaphor choices
#     n_ki = # number of times rater i predicted category k
#
#     # count instances of predicting category k for
#
#     p_e = (1 / (math.pow(n, 2))) * math.sum()


# yes this is a one-line function but I like the name and it
# is helping me semantically remember what this is so lay off
# my back, efficiency goblins
def get_total_annotations_per_track(track):
    return len(track.keys())

# get total annotations for a json-ified annotation file
def get_total_annotations_per_annotator(json_struct, to_diff):
    total_annotations = 0
    for track in to_diff:
        total_annotations += get_total_annotations_per_track(json_struct[track])
    return total_annotations

# goes into diff array and counts number of diffs
def count_diffs(diffs):
    if(diffs == None):
        return 0
    total_diffs = 0
    # for each diff
    for diff in diffs:
        # track that has diffs
        for trackName in diff.keys():
            total_diffs += len(diff[trackName])
    return total_diffs

# simple percentage calculation. Literally look at all total annotations, and see
# how many disagreed.
def compute_inter_annotator_agreement(json1, json2, track_diffs, to_diff):
    if(track_diffs == None):
        # No diffs, perfect agreement
        return 1

    total_annotations = get_total_annotations_per_annotator(json1, to_diff) + get_total_annotations_per_annotator(json2, to_diff)
    return (total_annotations - count_diffs(track_diffs)) / total_annotations


def compute_diffs(json1, json2, fn1="File1", fn2="File2", attributes=[]):
    if(not check_shape(json1, json2)):
        print "ERROR SHAPES ARE DIFFERENT"
        return

    track_diffs = []

    for key in json1.keys():
        diffs = compute_diffs_per_track(json1[key], json2[key], key, fn1, fn2, attributes)
        if diffs:
            track_diffs.append(diffs)

    if not track_diffs:
        return
    else:
        return track_diffs


def diff_files(f1, f2, spec="diff-spec.json", outfile="test-output.json"):
    json1 = build_json(f1)
    json2 = build_json(f2)

    spec_data = {}
    with open(spec, 'r') as s:
        spec_data = json.load(s)

    diffs = compute_diffs(json1, json2, f1, f2, spec_data)
    with open(outfile, 'w') as o:
        json.dump(diffs, o, indent=4, separators=(',', ': '), sort_keys=True)
        o.write('\n')

    return

def correlate_files(f1, specification, spec="correlation-spec.json", outfile="test-output.json"):
    file_json = build_json(f1)

    spec_data = {}
    with open(spec, 'r') as s:
        spec_data = json.load(s)

    correlations = calc_correlation(file_json, spec_data["tracks"], spec_data["attribute"])

    with open(outfile, 'w') as o:
        json.dump(correlations, o, indent=4, separators=(',', ': '), sort_keys=True)
        o.write('\n')


def jsonify_file(f1, outfile="test-output.json"):
    file_json = build_json(f1)

    with open(outfile, 'w') as o:
        json.dump(file_json, o, indent=4, separators=(',', ': '), sort_keys=True)
        o.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('-f1')
    parser.add_argument('-f2')
    parser.add_argument('-o', default="output.json", help="output file to store results in. Defaults to output.json")
    parser.add_argument('--diff', default=False, help="will look for spec that contains specifications for how to diff the annotations")
    parser.add_argument('--correlate', default=False, help="will look for spec that contains specifications for how to correlate")
    parser.add_argument('--jsonify', default=False, help="just JSONify f1")
    parser.add_argument('-spec', default="", help="name of specification file for correlation or diff")

    args = parser.parse_args()
    if args.diff:
        if not args.f2 or not args.spec:
            print "Error: must provide file to diff with and specification."
            exit(1)
        diff_files(args.f1, args.f2, args.spec, args.o)
    elif args.correlate:
        if not args.spec:
            print "Error: must provide a specification file to correlate with."
            exit(1)
        correlate_files(args.f1, args.spec, args.spec, args.o)
    elif args.jsonify:
        if not args.f1:
            print "Error: no file provided"
            exit(1)
        jsonify_file(args.f1, args.o)
