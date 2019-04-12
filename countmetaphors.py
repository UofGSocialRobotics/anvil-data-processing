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


## Building globals
def build_diff_attributes(names, attributes):
    track_attributes_to_diff = {}
    for name in names:
        ta_to_d = {
            "attributes": attributes
        }
        track_attributes_to_diff[name] = ta_to_d

    return track_attributes_to_diff

tracks_to_diff = [
    "Metaphor.Type1",
    "Metaphor.Type2",
    "Metaphor.Type3",
    "Metaphor"
]


attributes_to_diff = [
    "Metaphor"
]

track_attributes_to_diff = build_diff_attributes(tracks_to_diff, attributes_to_diff)




############ CUSTOM STUFF ############
######################################
## Lots of custom stuff to collapse ##
## tracks into one so that we can   ##
## compare multiple metaphors on    ##
## the same track                   ##
######################################

## Takes json that has dict for all the tracks you want to
## collapse, track name to collapse them into, and puts them all into one dict.
## Pretty sure it sorts by start time too <3 <3
## TODO test this. I think it actually doesn't, and instead relies on
## annotators using convention that tracks that represent same thing will
## be filled up from top to bottom
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
# TODO this gives you something good
def get_all_intratrack_correlations(json_struct, trackNames, attrs_to_diff=attributes_to_diff):
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
        while j < num_instances and float(instances[str(j)]["start"]) < float(cur_elem["end"]):
            print "FOUND OVERLAP"
            for attribute in attrs_to_diff:
                corr.append([cur_elem[attribute], instances[str(j)][attribute]])
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
        s = set()
        for item in elem:
            print item
            s.add(item)
        l.append(s)
    return l

## TODO have to figure out how to define "correlation" between metaphors.
## I think I should define it as likelihood of 1 metaphor occuring given
## that another metaphor has occurred
## Correlation will not be symmetric!
## One metaphor can make another more likely, but not necessarily the
## other way around.
# where A and B are metaphors,
# Bayes: P(A|B) = (P(B|A)P(A)) / P(B)
# P(A) = num occurances of A / total occurances
# P(B) = num occurances of B / total occurances
## TODO I think correlation can just be determined like this?
# P (A & B) / P(A) + P(B)
def calc_correlation(json_struct, trackNames):
    all_correlations = get_all_intratrack_correlations(json_struct, trackNames)
    # can change all of these to sets?
    all_correlations = list_of_lists_to_list_of_sets(all_correlations)
    return all_correlations



## so this deffo builds the json in a nice structure
def build_json(fileName):
    tree = ET.parse(fileName)
    json_structure = {}
    current_track = ""
    for elem in tree.iter():
        toPrint = [elem.tag, elem.text, elem.attrib]
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
    s1= elem1["start"]
    s2= elem2["start"]
    e1= elem1["end"]
    e2= elem2["end"]

    overlaps = False

    # majority of cases, get this out of the way
    if (s1 > e2 or s2 > e1):
        return False
    elif (s1 >= s2 and e2 >= s1):
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
def compute_diffs_from_reference_track(reference_track, comparison_track, trackName, fn1, fn2):
    track_diffs = []
    try:
        # TODO make track_attributes_to_diff dynamic
        track_to_diff = track_attributes_to_diff[trackName]
    # we don't actually care about diffing anything in this track
    except:
        print 'Excluding diff calculation for track ' + trackName
        return []
    try:
        tracks_to_diff["attributes"]
    except:
        # TODO do this
        print "Carolyn you need to make this dynamic"
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
def compute_diffs_per_track(track1, track2, trackName, fn1, fn2):
    # at first, assume independence. I can change it so it searches over all metaphors later.
    track_diffs = {}
    track_diffs[trackName] = []
    track_diffs[trackName].append(compute_diffs_from_reference_track(track1, track2, trackName, fn1, fn2))
    track_diffs[trackName].append(compute_diffs_from_reference_track(track2, track1, trackName, fn2, fn1))
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
# def count_instances_of_trackval(track, target_val):
#     count = 0
#     for key in track.keys():
#         if track[key]["Metaphor"] == target_val:
#             count += 1
#     return count


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

# diffs are formatted like this:
# [
#     {
#         "Track1": [
#             {diff},
#             {diff},
#         ]
#     },
#     {
#         "Track2": [
#             ...
#         ]
#     }
# ]
# so need to dig into structure a little more
def get_total_diffs(diffs):
    total_diffs = 0
    for diff in diffs:
        total_diffs += len(diff[diff.keys()[0]])

    return total_diffs

# yes this is a one-line function but I like the name and it
# is helping me semantically remember what this is so lay off
# my back, efficiency goblins
def get_total_annotations_per_track(track):
    return len(track.keys())


def get_total_annotations_per_annotator(json_struct, to_diff=tracks_to_diff):
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
# TODO revisit this as a proper mechanism for determining agreement
def compute_inter_annotator_agreement(json1, json2, track_diffs, to_diff=tracks_to_diff):
    if(track_diffs == None):
        # there are no diffs, so agreement is auto-perfect
        # TODO throw an error here instead
        return 1
    total_annotations = get_total_annotations_per_annotator(json1, to_diff) + get_total_annotations_per_annotator(json2, to_diff)
    return (total_annotations - count_diffs(track_diffs)) / total_annotations


def compute_diffs(json1, json2, fn1="File1", fn2="File2"):
    if(not check_shape(json1, json2)):
        print "ERROR SHAPES ARE DIFFERENT"
        return

    track_diffs = []
    for key in json1.keys():
        diffs = compute_diffs_per_track(json1[key], json2[key], key, fn1, fn2)
        if diffs:
            track_diffs.append(diffs)

    if not track_diffs:
        return
    else:
        # print "diffs:"
        # prettyPrint(track_diffs)
        return track_diffs


def read_file(fileName, comp_fileName):
    # might want to refactor this to include name
    json1 = build_json('test-annotation-1.anvil')
    json2 = build_json('test-annotation-2.anvil')

    diffs = compute_diffs(json1, json2, fileName, comp_fileName)
    prettyPrint(diffs)
    return diffs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('comp_file', nargs='?', type=argparse.FileType('r'))
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)

    args = parser.parse_args()
    read_file(args.infile, args.comp_file)
