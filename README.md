# anvil-data-processing
Python tools to take in and clean, flatten, and group ANVIL video annotation data together by fuzzy-timestamp and group label with JSON output structure as follows: 

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
$ python clean-data.py -f my_anvil_project.anvil -o my_cleaned_data_output.json

### Options
```
-f              # input file (anvil file to be processed)
-o              # output file 
--fuzzy N       # include to fuzzy match groups with timestamps within N MILLISECONDS of one another (start and end)
--sortbytime    # order groups by starting timestamp
```
