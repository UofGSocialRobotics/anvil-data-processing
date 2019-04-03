import argparse
import sys
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xmltodict
import json
from json import loads, dumps
from collections import OrderedDict

def prettyPrint(uglyJson):
    print(dumps(uglyJson, indent=4, sort_keys=True))

## so this deffo builds the json in a nice structure
def build_json(which_tho):
    tree = None
    if(which_tho == 1):
        tree = ET.parse('megyn-kelly-4.anvil')
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

def compute_diffs_per_track(track1, track2):
    prettyPrint(track1)
    prettyPrint(track2)
    # check for overlaps, basically
    # if any item doesn't have an overlap, it's a difference
    for elem1 in track1:
        for elem2 in track2:
            if()
    print


def compute_diffs(json1, json2):
    for key in json1.keys():
        compute_diffs_per_track(json1[key], json2[key])

    return


def read_file(fileName, comp_fileName):
    json1 = build_json(1)
    json2 = build_json(2)

    check_shape(json1, json2)

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
