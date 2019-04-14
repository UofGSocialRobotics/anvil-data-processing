ANVIL. It's a great video annotation tool but it lacks some functionality. This module addresses the fact that ANVIL produces pretty ugly (in my opinion) XML output, and currently lacks annotation-diff functionality (to compare two annotations of the same video). It also lacks the ability to correlate multiple overlapping attributes of the same type that may co-occur. 

We've gotten around this by using four tracks of the same type in order to code up to four simultaneous instances of a particular attribute in a track (in our case, metaphors used in gesture). This tool can take one or two ANVIL annotation files and perform correlational statistics on either intra-annotation tracks, or inter-annotator agreement. 

# anvil-data-processing
General purpose python tool to JSON-ify ANVIL, compare (and diff) two separate annotation files to calculate inter-annotator agreement, and provide inter-track correlation components (i.e. statistics on within-annotation track correlations). 

## Usages
### Options
```
-f1 [filename]                           # input file (anvil file to be processed)
-f2 [filename]                           #  OPTIONAL: input file (anvil file to be processed if diffing files
-o [filename]                            # output file (will be created if does not already exist)
-spec [spec_filename]                    # name of file for either diff or correlation spec
--diff [True | False]                    # default False. Diff f1 and f2 (spec must be provided)
--correlate [True | False]               # default False. Correlate something about f1 (spec must be provided)
--jsonify [True | False]                 # default False. Just build JSON 
```

### Example: JSON-ifying data

example usage of JSON-ifying ANVIL data
`$ python diff_correlate.py -f1 annotator_1.anvil -o annotator_1.json --jsonify True`

ex. if Anvil data looks like this:
```
<track name="Type1" type="primary"
    <el index="0" start="101.2" end="103.53">
        <attribute name="labelA">5</attribute>
        <attribute name="labelB">this is a quote from the video</attribute>
        <attribute name="labelC">this is custom datatype 0</attribute>
    </el>
    ...
</track>
<track name="Type2" time="primary">
    <el index="0" start="105.2" end="106.98">
        <attribute name="labelD">this is another custom datatype</attribute>
        <attribute name="labelE">False</attribute>
    </el>
</track>
...
```

JSON data (in annotator_1.json) will look like this:
```
{
    "Type1": {
        "0": {
            "labelA": 5,
            "labelB": "this is a quote from the video",
            "labelC": "this is custom datatype 0",
            "end": "103.53",
            "start": "101.2"
        },
        ...
    },
    "Type2": {
        "0": {
            "labelD": "this is another custom datatype",
            "labelE": False,
            "end": "106.58",
            "start": "105.20"
        }
    },
    ...
}
```

### Example: Getting inter-annotator agreement
Produces output that includes both the raw agreement, as well as each set of diffs per track. If annotations at specific areas overlap with different values (based on attributes in the diff spec), that is counted as a diff. If an annotation occurs in one file and not the other, the diff reports there is no corresponding annotation found at that timestamp in the indicated file. 

#### Usage:
```
$ python diff_correlate.py -f1 test-annotation-1.anvil -f2 test-annotation-2.anvil -o diffs.json --diff True -spec diff-spec.json
```

#### Example Output:
```
{
    "Agreement": # A float (0-1) that represents inter-annotator correlation based on the diffspec
    "Diffs": [
        "Track1": [
            {
                "File1": {
                    "Attribute1": "0",
                    "Attribute2": "Foo",
                    "end": "22",
                    "start": "19"
                },
                "File2": {
                    "Attribute1": "2",
                    "Attribute2": "Bar",
                    "end": "21",
                    "start": "18"            
                }
            },
            {
                "File1": {
                    "Attribute1": "0",
                    "Attribute2": "Biz",
                    "end": "29",
                    "start": "26"
                },
                "File2": "No corresponding annotation found"
            }        

        ],
        "Track2": ...
    ]
}
```
Note inter-annotator agreement is calculated only based on the spec provided (the diffs that are generated)


### Example: Getting intra-annotation statistics
Calculates inter-track correlation for specific attributes based on the correlation spec. This happens by correlating a particular attribute value with all other attribute values with which it co-occurs, and comparing that number to total times the attribute has that value. **If a particular value never co-occurs with any other value in the annotation file, it will not show up in this list.**

#### Usage:
```
python diff_correlate.py -f1 test-annotation-1.anvil -o correlations.json --correlate True -spec correlation-spec.json
```

#### Example output:
```
{
    "abstract idea is concrete object": {
        "certain is firm": 1.0
    },
    "certain is firm": {
        "abstract idea is concrete object": 1.0,
        "change is motion": 1.0
    },
    "change is motion": {
        "certain is firm": 0.5
    }
}
```

## Spec Files
Video annotations are often rife with many specific elements that we know won't be exactly the same with each annotator. To account for this, this tool requires specifications for how to diff annotations (while staying sensible). 

### Diff Spec
In the diff spec, you need to include the name of the tracks you want to include, as well as all of the attributes of those tracks you want to diff. It assumes each track is independent. 

#### Example Diff Spec:
```
{
  "Track1": {
    "attributes": [
      "Foo",
      "Bar"
      ]
    },
  "Track2": {
    "attributes": [
      "Biz"
    ]
  },
  "Track3": {
    "attributes": [
      "Bam"
    ]
  }
}

```

### Correlation Spec
The correlation spec is meant to compare the same attribute across multiple tracks (when a particular event can overlap with another event of the same type). To correlate, you must provide the tracks across which to compare the attribute, and the attribute name you wish to correlate. 

#### Example Correlation Spec:
```
{
  "tracks": [
    "Metaphor.Type1",
    "Metaphor.Type2",
    "Metaphor.Type3"
  ],
  "attribute": "Metaphor"
}
```

## TESTING
To run unit tests please run 
```
$ python unit-tests.py
> ----------------------------------------------------------------------
Ran 42 tests in 0.007s

OK
```
if output is anything less than spectacular, yell loudly and file an issue in the repo. 


