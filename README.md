this really will end up being multiple programs

# anvil-data-processing
Python tools to take in and clean, flatten, and group ANVIL video annotation data together by fuzzy-timestamp and group label with JSON output structure described below. Also provides computation specific to metaphor counting. For example, counts instances of particular metaphors, and most common metaphor overlaps.

ex. if Anvil data looks like this:
```
<el index="39" start="101.2" end="103.53">
    <attribute name="labelA-0">5</attribute>
    <attribute name="labelA-1">this is a quote from the video</attribute>
    <attribute name="labelA-2">this is custom datatype 0</attribute>
</el>
...
<el index="83" start="100.08" end="104.53">
    <attribute name="labelB-0">Speaker 0</attribute>
    <attribute name="labelB-1">0</attribute>
</el>
```

JSON data will look like this:
```
{
  timestampGroups: [
      ...
      {
          "Group39-83": {
              "startAvg:" 100.64
              "endAvg": 104.64
              "duration": 4
              "labels": {
                  "labelA-0": 5
                  "labelA-1": "this is a quote from the video"
                  "labelA-2": "this is custom datatype 0"
                  "labelB-0": "Speaker 0"
                  "labelB-1": 0
              }
          }
      },
      ...
  ]
}
```

## Usage
$ python input.py my_anvil_project.anvil my_cleaned_data_output.json [--fuzzy N] [--sortbytime T/F]

### Options
```
-f              # input file (anvil file to be processed)
-o              # output file
--fuzzy N       # include to fuzzy match groups with timestamps within N MILLISECONDS of one another (start and end)
--full          # provide full output
```

For instance 
```
$ python count-metaphors.py -f my_anvil_project.anvil -o metaphors.json
```
Will write JSON with this shape to metaphors.json
```
{
    metadata: {
        most_common: String                 // will be string of the most common metaphors
        most_common_count:  int             // will be int of number of times this metaphor occurred
        most_common_overlap: {
            metaphors: [
                String,
                String
            ]
            count:                          // int
        }
    },
    metaphors: [
        {
            metaphor: String
            count: int
            overlaps: [
                {
                    metaphor_overlap: String    // String of which metaphor overlapped this one
                    count: int                  // count of number of times this overlap occurred
                },
            ]
            
        },
    ]
}
```


