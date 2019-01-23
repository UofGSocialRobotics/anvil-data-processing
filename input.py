import argparse
import sys
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xmltodict
from json import loads, dumps
from collections import OrderedDict

def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))

def add_data(name, track_dict):
    if(name == 'Metaphor.Type3' or name == 'Metaphor.Type4'):
        print len(track_dict)
        print track_dict

def process_raw_track(track):
    processed_track = {}
    processed_track['name'] = track[0][1]
    n = processed_track['name']
    processed_track['type'] = track[1][1]
    track_data = to_dict(track[2][1])
    if(n == 'Metaphor.Type3' or n == 'Metaphor.Type4'):
        print track_data

    entry = {}
    if isinstance(track_data, list):
        for instance in track_data:
            entry = add_data(processed_track['name'], instance)
    else:   # there's only one entry
        entry = add_data(processed_track['name'], entry)

    # print entry
    processed_track['attributes'] = entry
    # print processed_track

def deep_print(d):
    if isinstance(d, dict):
        for k,v in d.items():
            print k
            deep_print(v)
    elif isinstance(d, list):
        for elem in d:
            deep_print(elem)
    else:
        print d


def read_file(fileName):
    print(fileName)
    # get the raw data as big old ugly list
    raw = xmltodict.parse(fileName).items()[0][1].items()
    rawDict = to_dict(raw)
    deep_print(rawDict[1])
    # get some useful metadata
    # metadata = raw[0][1].items()
    # specificationFileName = metadata[0][1].items()[0][1]
    # videoName = metadata[1][1].items()[0][1]
    # coder = metadata[2][1][0].items()[2][1]
    #
    # # parse out group sections
    # rawTracks = raw[1][1].items()[0][1]
    # tracks = []
    # # gross here, should do something clever about recursing instead of
    # # making this specific to my annotation scheme
    # for track in rawTracks:
    #     t = process_raw_track(track.items())
    #     tracks.append(t)
    # print

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some inputs.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument('--fuzzy', type=int, default=0,
                        help='fuzzy match groups within N milliseconds')
    parser.add_argument('--sortbytime', type=bool, default=False,
                        help='order groups by starting timestamp')

    args = parser.parse_args()
    read_file(args.infile)
