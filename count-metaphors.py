import argparse
import sys
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xmltodict
from json import loads, dumps
from collections import OrderedDict

def process_metaphor_tracks(tracks):
    metaphor_collector = {}               # this will be a {metaphor: count} dict
    full_output = {}

    for track in tracks:
        metaphor_collector = count_metaphors_per_track(metaphor_collector, track)

    add_overlaps(metaphor_collector)



def count_metaphors_per_track(metaphor_collector, track):
    for element in track['el']:
        for attr in element['attribute']:
            if attr['@name'] == 'Metaphor':
                metaphor = attr['#text']
                if(metaphor in metaphor_collector.keys()):
                    metaphor_collector[metaphor]['count'] = metaphor_collector[metaphor]['count'] + 1
                else:
                    metaphor_collector[metaphor] = {}
                    metaphor_collector[metaphor]['count'] = 1
                    metaphor_collector[metaphor]['startend_pairs'] = []
                    metaphor_collector[metaphor]['overlaps'] = []

        # collect start/ends for later
        metaphor_collector[metaphor]['startend_pairs'].append({'start': element['@start'], 'end': element['@end']})

    return metaphor_collector


def add_overlaps(metaphor_collector):
    for k,v in metaphor_collector.iteritems():
        for k2,v2 in metaphor_collector.iteritems():
            if v == v2:                         # ignore overlaps with ourselves
                break
            num_overlaps = count_overlaps(v['startend_pairs'], v2['startend_pairs'])
            for i in range(0, num_overlaps):
                v['overlaps'].append(k2)
    clean_overlaps(metaphor_collector)


def count_overlaps(group1pairs, group2pairs):
    overlaps = 0
    for sepair in group1pairs:
        for sepair2 in group2pairs: 
            # now actually check if they overlap
            s1 = float(sepair['start'])
            e1 = float(sepair['end'])
            s2 = float(sepair2['start'])
            e2 = float(sepair2['end'])
            if((s2 - e1 <= 0) or
               (s1 - e2 <= 0)):
                overlaps+=1

    return overlaps


# takes array of dictionaries and returns array of all keys in top level dictionaries from array
def clean_overlaps(metaphor_collector):
    for k, v in metaphor_collector.iteritems():
        print k



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