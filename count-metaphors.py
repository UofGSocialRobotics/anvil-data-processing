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

def process_metaphor_tracks(tracks):
    metaphor_counter = {}               # this will be a {metaphor: count} dict

    for track in tracks:
        metaphor_counter = count_metaphors_per_track(metaphor_counter, track)

    print metaphor_counter



def count_metaphors_per_track(metaphor_counter, track):
    for element in track['el']:
        for attr in element['attribute']:
            try:      
                if attr['@name'] == 'Metaphor':
                    metaphor = attr['#text']
                    if(metaphor in metaphor_counter.keys()):
                        metaphor_counter[metaphor] = metaphor_counter[metaphor] + 1
                    else:
                        metaphor_counter[metaphor] = 1
            except:
                print attr
    return metaphor_counter


def recurse_elements(track):
    print



def read_file(fileName):
    with open('megyn-kelly-4.anvil') as fd:
        doc = xmltodict.parse(fd.read())
        tracks = doc['annotation']['body']['track']
        process_metaphor_tracks(tracks[:4])



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