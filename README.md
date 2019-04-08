ANVIL, it's a great video annotation tool but it lacks some functionality. This module addresses the fact that ANVIL produces pretty ugly (in my opinion) XML output, and currently lacks annotation-diff functionality (to compare two annotations of the same video). It also lacks the ability to code multiple overlapping attributes of the same type that may co-occur. 

We've gotten around this by using four tracks of the same type in order to code up to four simultaneous instances of a particular attribute in a track (in our case, metaphors used in gesture). This tool can take one or two ANVIL annotation files and perform correlational statistics on either intra-annotation tracks, or inter-annotator agreement. 

# anvil-data-processing
General purpose python tool to JSON-ify ANVIL and compare two separate annotation files to calculate inter-annotator agreement. Also provides inter-track correlation components (i.e. statistics on within-annotation track correlations). 

## Usages
### Options
```
-f <filename>                           # input file (anvil file to be processed)
-o <filename>                           # output file (will be created if does not already exist)
--comp_file <filename>                  # file to compare if want inter-annotator agreement
--correlate <track1> <track2> ...       # list of track names within file to calculate correlations between
```

## Example: JSON-ifying data

example usage of JSON-ifying ANVIL data
`$ python countmetaphors.py -f annotator_1.anvil -o annotator_1.json`

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

## Example: Getting inter-annotator agreement
` $ python countmetaphors.py -f my_anvil_project.anvil -o my_cleaned_data_output.json `

For instance 
```
$ python count-metaphors.py -f annotator_1.anvil -o annotation_diffs.json --comp_file annotator_2.anvil
```
Produces output in the form of
```
{
    "Metadata": {   
        InterAnnotatorAgreement: {
            "track1": Number (0-1)
            "track2": Number (0-1)
            ...     # for all tracks
            "Average": Number(0-1)
        }
    },
    "Diffs": [
        "track1": [
            {
                "file1": {
                    # track attributes
                },
                "file2": "No corresponding annotation found"    # OR track attributes that differ in file2
            },
            {
                "file1": "No corresponding annotation found",
                "file2": {
                    # track attributes
                }
            }
        ],
        "track2": [
            {
                "file1": {
                    # track attributes
                }
                "file2": {
                    # track attributes
                }
            }            
        ]
    ]
}
```

So the example above may produce output such as
```
{
    "Metadata": {   
        InterAnnotatorAgreement: {
            "Type1": 0.87
            "Type2": 0.56
            ...
            "Average": 0.76
        }
    },
    "Diffs": [
        "Type1": [
            {
                "annotator_1": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "end": "2",
                    "start": "1"
                },
                "annotator_2": "No corresponding annotation found"
            },
            {
                "annotator_1": "No corresponding annotation found",
                "annotator_2": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "end": "4",
                    "start": "3"
                }
            }
        ],
        "Type2": [
            {
                "annotator_1": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "end": "4",
                    "start": "2"
                }
                "annotator_2": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "end": "5",
                    "start": "3"
                }
            }            
        ]
    ]
}
```
Note that inter-annotator difference is computed by finding overlaps within the same track and searching for differences within them. 


## Example: Getting intra-annotation statistics
 TODO

