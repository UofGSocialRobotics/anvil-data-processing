import argparse
import sys
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xmltodict
import json
from json import loads, dumps
from collections import OrderedDict



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
    "Metaphor.Type4",
]

attributes_to_diff = [
    "Metaphor"
]

track_attributes_to_diff = build_diff_attributes(tracks_to_diff, attributes_to_diff)
prettyPrint(track_attributes_to_diff)
#     {
#         "track_name": "Metaphor.Type1",
#         "attributes": [
#             "Metaphor"
#         ]
#     },
#     {
#         "track_name": "Metaphor.Type2",
#         "attributes": [
#             "Metaphor"
#         ]
#     },
#     {
#         "track_name": "Metaphor.Type3",
#         "attributes": [
#             "Metaphor"
#         ]
#     },
#     {
#         "track_name": "Metaphor.Type4",
#         "attributes": [
#             "Metaphor"
#         ]
#     },
# ]

## so this deffo builds the json in a nice structure
def build_json(which_tho):
    tree = None
    if(which_tho == 1):
        tree = ET.parse('megyn-kelly-4-plus2.anvil')
    else:
        tree = ET.parse('megyn-kelly-4-plus1.anvil')
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
            #print elem.attrib
            json_structure[current_track][current_index][elem.attrib["name"]] = elem.text

    return(json_structure)

def check_shape(json1, json2):
    if(set(json1.keys()) != set(json2.keys())):
        return False
    return True

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

def compute_diffs_from_reference_track(reference_track, other_track, trackName):
    # check for overlaps, basically
    # if any item doesn't have an overlap, it's a difference
    # at first, assume independence. I can change it so it searches over all metaphors later.
    track_diffs = []
    try:
        track_to_diff = track_attributes_to_diff[trackName]
    # we don't actually care about diffing anything in this track
    except:
        print 'Excluding diff calculation for track ' + trackName
        return []
    attributes_to_diff = track_to_diff["attributes"]
    # nested for loop, not my finest work.
    for elem1 in reference_track:
        t1 = reference_track[elem1]
        found_diff = True
        no_overlaps = True
        for elem2 in other_track:
            t2 = other_track[elem2]
            # also need to tell it what attributes to pay attention to
            for attribute in attributes_to_diff:
                # if we find something overlapping here, it's not a difference
                if overlaps(t1, t2):
                    no_overlaps = False
                    if t1[attribute] == t2[attribute]:
                        found_diff = False
        if found_diff:
            diff = {}
            if no_overlaps:
                diff = {
                    "File1": t1,
                    "File2": "No corresponding annotation found"
                }
            else:
                diff = {
                    "File1": t1,
                    "File2": t2
                }
            track_diffs.append(diff)

    return track_diffs



## hmm so right now this works but it's non-symmetric.
def compute_diffs_per_track(track1, track2, trackName):
    # at first, assume independence. I can change it so it searches over all metaphors later.
    track_diffs = {}
    track_diffs[trackName] = []
    track_diffs[trackName].append(compute_diffs_from_reference_track(track1, track2, trackName))
    track_diffs[trackName].append(compute_diffs_from_reference_track(track2, track1, trackName))
    track_diffs[trackName] = flatten(track_diffs[trackName])
    if not track_diffs[trackName]:
        # return None if empty list
        return
    return track_diffs


def compute_diffs(json1, json2):
    track_diffs = []
    for key in json1.keys():
        diffs = compute_diffs_per_track(json1[key], json2[key], key)
        if diffs:
            track_diffs.append(diffs)
    if not track_diffs:
        print "No diffs were found in the annotation files"
    else:
        print "Diffs were found in annotation file:"
        prettyPrint(track_diffs)
    return


def read_file(fileName, comp_fileName):
    json1 = build_json(1)
    json2 = build_json(2)

    if(not check_shape(json1, json2)):
        print "ERROR SHAPES ARE DIFFERENT"

    compute_diffs(json1, json2)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('comp_file', nargs='?', type=argparse.FileType('r'))
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument('--fuzzy', type=int, default=0,
                        help='fuzzy match groups within N milliseconds')
    parser.add_argument('--sortbytime', type=bool, default=False,
                        help='order groups by starting timestamp')

    args = parser.parse_args()
    read_file(args.infile, args.comp_file)
