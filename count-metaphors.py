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
def build_json():
    tree = ET.parse('megyn-kelly-4.anvil')
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
    prettyPrint(json_structure)


def compute_diffs(metas1, metas2):
    print metas1
    print
    print metas2
    return


def read_file(fileName, comp_fileName):
    test_iterate()
    # comp_fileName = True
    # with open('megyn-kelly-4.anvil') as fd:
    #     doc = xmltodict.parse(fd.read())
    #     tracks = doc['annotation']['body']['track']
    #     metaphors = get_metaphor_collector(tracks)
    #
    #     if(comp_fileName):
    #         with open('megyn-kelly-4-plus1.anvil') as compfile:
    #             comp_doc = xmltodict.parse(compfile.read())
    #             comp_tracks = comp_doc['annotation']['body']['track']
    #             comp_metaphors = get_metaphor_collector(comp_tracks)
    #             compute_diffs(metaphors, comp_metaphors)
    # return



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
