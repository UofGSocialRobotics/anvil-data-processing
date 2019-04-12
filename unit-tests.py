import unittest
from countmetaphors import *


class TestStringMethods(unittest.TestCase):
    ## TODO
    # Test:
    # build_json
    # read_file

    ## OVERLAPS ##
    def test_overlap(self):
        i1 = {
            'start': 1,
            'end': 2
        }
        i2 = {
            'start': 3,
            'end': 4
        }
        self.assertFalse(overlaps(i1, i2))
    def test_overlap_symmetrical(self):
        i1 = {
            'start': 3,
            'end': 4
        }
        i2 = {
            'start': 1,
            'end': 2
        }
        self.assertFalse(overlaps(i1, i2))
    def test_overlap_edge(self):
        i1 = {
            'start': 1,
            'end': 2
        }
        i2 = {
            'start': 2,
            'end': 3
        }
        self.assertTrue(overlaps(i1, i2))
    def test_overlap_edge_symmetrical(self):
        i1 = {
            'start': 2,
            'end': 3
        }
        i2 = {
            'start': 1,
            'end': 2
        }
        self.assertTrue(overlaps(i1, i2))
    def test_overlap_front_edge(self):
        i1 = {
            'start': 2,
            'end': 4
        }
        i2 = {
            'start': 1,
            'end': 3
        }
        self.assertTrue(overlaps(i1, i2))
    def test_overlap_back_edge(self):
        i1 = {
            'start': 2,
            'end': 4
        }
        i2 = {
            'start': 3,
            'end': 5
        }
        self.assertTrue(overlaps(i1, i2))
    def test_overlap_middle(self):
        i1 = {
            'start': 1,
            'end': 4
        }
        i2 = {
            'start': 2,
            'end': 3
        }
        self.assertTrue(overlaps(i1, i2))
    def test_overlap_surround(self):
        i1 = {
            'start': 2,
            'end': 3
        }
        i2 = {
            'start': 1,
            'end': 4
        }
        self.assertTrue(overlaps(i1, i2))

    ## Checking the shape of the annotations
    def test_shape_layer_one(self):
        i1 = {
            "test1": [],
            "test2": {}
        }
        i2 = {
            "test1": [],
            "test2": {}
        }
        self.assertTrue(check_shape(i1, i2))
    def test_shape_layer_one_type(self):
        i1 = {
            "test1": {},
            "test2": {}
        }
        i2 = {
            "test1": [],
            "test2": {}
        }
        self.assertFalse(check_shape(i1, i2))
    def test_shape_layer_one_type_symmetric(self):
        i1 = {
            "test1": [],
            "test2": []
        }
        i2 = {
            "test1": [],
            "test2": {}
        }
        self.assertFalse(check_shape(i1, i2))
    def test_shape_layer_two(self):
        i1 = {
            "test1": [],
            "test2": {
                "test3": ""
            }
        }
        i2 = {
            "test1": [],
            "test2": {}
        }
        self.assertFalse(check_shape(i1, i2))
    def test_shape_empty(self):
        i1 = {}
        i2 = {
            "test1": [],
            "test2": {}
        }
        self.assertFalse(check_shape(i1, i2))
    def test_shape_extra_attrs(self):
        i1 = {
            "test1": []
        }
        i2 = {
            "test1": [],
            "test2": {}
        }
        self.assertFalse(check_shape(i1, i2))
    def test_shape_data_doesnt_matter(self):
        i1 = {
            "test1": ["Hello", "How are you"],
            "test2": {}
        }
        i2 = {
            "test1": ["I'm", "In", "California", "Dreaming"],
            "test2": {}
        }
        self.assertTrue(check_shape(i1, i2))
    def test_shape_one_examples(self):
        i1 = build_json('test-annotation-1.anvil')
        i2 = build_json('test-annotation-1.anvil')
        self.assertTrue(check_shape(i1, i2))

    def test_shape_two_examples(self):
        i1 = build_json('test-annotation-1.anvil')
        i2 = build_json('test-annotation-2.anvil')
        self.assertTrue(check_shape(i1, i2))

    ## Checking some pre-made test annotations
    def test_shape_spec1(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "",
                    "start": "",
                    "end": ""
                }
            },
            "Metaphor.Type2": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "",
                    "start": "",
                    "end": ""
                }
            },
            "Metaphor.Type3": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "",
                    "start": "",
                    "end": ""
                }
            },
        }
        i2 = build_json('test-annotation-1.anvil')
        self.assertTrue(check_shape(i1, i2))

    ## Testing diff functionality now
    def test_diff_bad_shape(self):
        i1 = {
            "Metaphor.Type1": [],
            "Metaphor.Type2": []
        }
        i2 = {
            "Metaphor.Type1": [],
            "Metaphor.Type2": {}
        }
        self.assertIsNone(compute_diffs(i1, i2))

    def test_diff_simple_same(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        i2 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        self.assertIsNone(compute_diffs(i1, i2))

    def test_diff_simple_diff_nooverlap(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        i2 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "3",
                    "end": "4"
                }
            }
        }
        self.assertIsNotNone(compute_diffs(i1, i2, "Nooverlap1", "Nooverlap2"))

    def test_diff_simple_diff_overlap(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        i2 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1.5",
                    "end": "2.5"
                }
            }
        }
        self.assertIsNone(compute_diffs(i1, i2))

    def test_diff_simple_diff_metaphor(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        i2 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "start": "1.5",
                    "end": "2.5"
                }
            }
        }
        self.assertIsNotNone(compute_diffs(i1, i2, "Test1", "Test2"))

    ## build_json
    # def test_build_json(self):
    #     prettyPrint(build_json('test-annotation-1.anvil'))

    ## Combine Tracks oh jesus
    def test_collapse_tracks(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "0.2",
                    "end": "1.3"
                }
            },
            "Metaphor.Type2": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "start": "1",
                    "end": "2"
                }
            },
            "Metaphor.Type3": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test3",
                    "start": "1",
                    "end": "2"
                }
            },
            "Metaphor.Type4": {
                "0": {
                    "Confidence": "",
                    "start": "",
                    "end": "",
                }
            }
        }


        expected_output = {
            "Metaphor.Type4": {
                "0": {
                    "Confidence": "",
                    "end": "",
                    "start": ""
                }
            },
            "Metaphors": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "end": "1.3",
                    "start": "0.2"
                },
                "1": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "end": "2",
                    "start": "1"
                },
                "2": {
                    "Confidence": "",
                    "Metaphor": "test3",
                    "end": "2",
                    "start": "1"
                }
            }
        }

        actual_output = collapse_tracks(i1, "Metaphors", ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        self.assertEqual(actual_output.keys(), expected_output.keys())
        self.assertEqual(actual_output.keys(), ["Metaphor.Type4", "Metaphors"])
        self.assertEqual(actual_output["Metaphors"].keys(), expected_output["Metaphors"].keys())

    # TODO test actual known diffs
    # def test_actual_diffs(self):
    #     read_file('File1', 'File2')

    ## lol these are more like integration tests
    def integration_build_collapse(self):
        self.assertEqual(collapse_tracks(build_json('test-annotation-1.anvil')), collapse_tracks(build_json('test-annotation-2.anvil')))


    ##
    ## test annotator agreements
    def test_count_annotations_per_track(self):
        i1 = {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                },
                "1": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            }
        self.assertEqual(2, get_total_annotations_per_track(i1))

    ## test counting
    def test_count_annotations_per_track(self):
        i1 = build_json('test-annotation-1.anvil')
        self.assertEqual(2, get_total_annotations_per_track(i1['Metaphor.Type1']))


    def test_count_annotations_per_annotator(self):
        i1 = build_json('test-annotation-1.anvil')
        self.assertEqual(4, get_total_annotations_per_annotator(i1, ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3']))

    ## test annotator agreements
    def test_agreement_no_diffs(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                },
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "3",
                    "end": "5"
                }
            }
        }
        i2 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1.5",
                    "end": "2.5"
                }
            }
        }
        self.assertEqual(1, compute_inter_annotator_agreement(i1, i2, [], ['Metaphor.Type1']))


    def test_agreement_some_diffs(self):
        i1 = build_json('test-annotation-1.anvil')
        i2 = build_json('test-annotation-2.anvil')
        diffs = compute_diffs(i1, i2)
        prettyPrint(diffs)
        self.assertEqual(0.85, compute_inter_annotator_agreement(i1, i2, diffs, ['Metaphor.Type1']))


    def test_agreement_some_diffs(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        i2 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "start": "1.5",
                    "end": "2.5"
                }
            }
        }

        diffs = [
            {
                "Metaphor.Type1": [
                    {
                        "Test1": {
                            "Confidence": "",
                            "Metaphor": "test1",
                            "end": "2",
                            "start": "1"
                        },
                        "Test2": {
                            "Confidence": "",
                            "Metaphor": "test2",
                            "end": "2.5",
                            "start": "1.5"
                        }
                    }
                ]
            }
        ]
        self.assertEqual(0.5, compute_inter_annotator_agreement(i1, i2, diffs, ['Metaphor.Type1']))

    def test_agreement_full_files(self):
        i1 = build_json('test-annotation-1.anvil')
        i2 = build_json('test-annotation-2.anvil')
        diffs = compute_diffs(i1, i2)
        self.assertEqual(0.7, compute_inter_annotator_agreement(i1, i2, diffs, ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3']))

    def test_collapse_file1(self):
        expected = {
            "Metaphor": {
                "0": {
                    "Confidence": "0",
                    "Metaphor": "abstract idea is concrete object",
                    "end": "3.64",
                    "start": "1.64"
                },
                "1": {
                    "Confidence": "0",
                    "Metaphor": "certain is firm",
                    "end": "4.92",
                    "start": "2.8"
                },
                "2": {
                    "Confidence": "0",
                    "Metaphor": "change is motion",
                    "end": "6.28",
                    "start": "4.6"
                },
                "3": {
                        "Confidence": "0",
                        "Metaphor": "change is motion",
                        "end": "13.12",
                        "start": "11.52"
                }
            }
        }
        i1 = build_json('test-annotation-1.anvil')
        i2 = collapse_tracks(i1, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        self.assertEqual(expected, i2)


    def test_count_equals_collapsed_track(self):
        i1 = build_json('test-annotation-1.anvil')
        i2 = collapse_tracks(i1, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        total_raw = get_total_annotations_per_annotator(i1, ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        total_collapsed = get_total_annotations_per_annotator(i2, ['Metaphor'])
        self.assertEqual(total_raw, total_collapsed)


    def test_agreement_collapsed_same_track(self):
        i1 = build_json('test-annotation-1.anvil')
        i2 = collapse_tracks(i1, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        expected = {
            "Metaphor": {
                "0": {
                    "Confidence": "0",
                    "Metaphor": "abstract idea is concrete object",
                    "end": "3.64",
                    "start": "1.64"
                },
                "1": {
                    "Confidence": "0",
                    "Metaphor": "certain is firm",
                    "end": "4.92",
                    "start": "2.8"
                },
                "2": {
                    "Confidence": "0",
                    "Metaphor": "change is motion",
                    "end": "6.28",
                    "start": "4.6"
                },
                "3": {
                        "Confidence": "0",
                        "Metaphor": "change is motion",
                        "end": "13.12",
                        "start": "11.52"
                }
            }
        }
        diffs = compute_diffs(i2, expected)
        self.assertEqual(1, compute_inter_annotator_agreement(expected, i2, diffs, ['Metaphor']))

    def test_collapsed_diff_count_is_same_as_raw_diff(self):
        i1 = build_json('test-annotation-1.anvil')
        i2 = build_json('test-annotation-2.anvil')
        raw_diff = compute_diffs(i1, i2)
        i1_collapsed = collapse_tracks(i1, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        i2_collapsed = collapse_tracks(i2, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        collapsed_diff = compute_diffs(i1_collapsed, i2_collapsed)

        self.assertEqual(count_diffs(raw_diff), count_diffs(collapsed_diff))


    def test_collapsed_agreement_is_raw_agreement(self):
        i1 = build_json('test-annotation-1.anvil')
        i2 = build_json('test-annotation-2.anvil')
        raw_diff = compute_diffs(i1, i2)
        i1_collapsed = collapse_tracks(i1, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        i2_collapsed = collapse_tracks(i2, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        collapsed_diff = compute_diffs(i1_collapsed, i2_collapsed)
        raw_agreement = compute_inter_annotator_agreement(i1, i2, raw_diff, ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        collapsed_agreement = compute_inter_annotator_agreement(i1_collapsed, i2_collapsed, collapsed_diff, ['Metaphor'])

        self.assertEqual(raw_agreement, collapsed_agreement, 0.7)


    def test_collapse_single_track(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                },
                "1": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "3",
                    "end": "4"
                }
            }
        }
        expected = {
            "Metaphor": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "end": "2",
                    "start": "1"
                },
                "1": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "end": "4",
                    "start": "3"
                }
            }
        }
        i1_collapsed = collapse_tracks(i1, 'Metaphor', ['Metaphor.Type1'])
        self.assertEqual(i1_collapsed, expected)

    def test_collapsed_agreement_is_raw_agreement_toy_null(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            },
            "Metaphor.Type2": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        i2 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            },
            "Metaphor.Type2": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        raw_diff = compute_diffs(i1, i2)
        i1_collapsed = collapse_tracks(i1, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2'])
        i2_collapsed = collapse_tracks(i2, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2'])
        collapsed_diff = compute_diffs(i1_collapsed, i2_collapsed)
        prettyPrint(raw_diff)
        prettyPrint(collapsed_diff)
        self.assertEqual(raw_diff, collapsed_diff)


    # TODO this test is broken. It should return 0
    # what it should do is count as 2 diffs for every
    # time there is an actual diff between the files,
    # and one when there's no corresponding annotation found
    def test_collapsed_agreement_is_raw_agreement_toy(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test1",
                    "start": "1",
                    "end": "2"
                }
            },
            "Metaphor.Type2": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "start": "3",
                    "end": "4"
                }
            }
        }
        i2 = {
            "Metaphor.Type1": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test3",
                    "start": "1",
                    "end": "2"
                }
            },
            "Metaphor.Type2": {
                "0": {
                    "Confidence": "",
                    "Metaphor": "test2",
                    "start": "1",
                    "end": "2"
                }
            }
        }
        raw_diff = compute_diffs(i1, i2)
        i1_collapsed = collapse_tracks(i1, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2'])
        i2_collapsed = collapse_tracks(i2, 'Metaphor', ['Metaphor.Type1', 'Metaphor.Type2'])
        prettyPrint(raw_diff)
        collapsed_diff = compute_diffs(i1_collapsed, i2_collapsed)
        prettyPrint(collapsed_diff)
        self.assertEqual(count_diffs(raw_diff), count_diffs(collapsed_diff))
        raw_agreement = compute_inter_annotator_agreement(i1, i2, raw_diff, ['Metaphor.Type1', 'Metaphor.Type2'])
        collapsed_agreement = compute_inter_annotator_agreement(i1_collapsed, i2_collapsed, collapsed_diff, ['Metaphor'])
        self.assertEqual(raw_agreement, collapsed_agreement)
        self.assertEqual(raw_agreement, 0.25)


    ## Start testing intra-track correlation
    def test_all_intracorrelation(self):
        i1 = build_json('test-annotation-2.anvil')
        expected = [
            [
                "abstract idea is concrete object",
                "certain is firm"
            ],
            [
                "certain is firm",
                "importance is size"
            ],
            [
                "change is motion",
                "accessible is open"
            ]
        ]
        corrs = get_all_intratrack_correlations(i1, ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        self.assertEqual(corrs, expected)

    ## Start testing intra-track correlation
    def test_intracorrelation_calcs(self):
        i1 = build_json('test-annotation-2.anvil')
        expected = [
            [
                "abstract idea is concrete object",
                "certain is firm"
            ],
            [
                "certain is firm",
                "importance is size"
            ],
            [
                "change is motion",
                "accessible is open"
            ]
        ]
        corrs = get_all_intratrack_correlations(i1, ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'])
        self.assertEqual(corrs, expected)



    def test_get_total_occurances_toy(self):
        i1 = {
            "Metaphor.Type1": {
                "0": {
                    "Metaphor": "certain is firm"
                },
                "1": {
                    "Metaphor": "time is a line"
                },
                "2": {
                    "Metaphor": "change is motion"
                },
            },
            "Metaphor.Type2": {
                "0": {
                    "Metaphor": "certain is firm"
                }
            },
            "Metaphor.Type3": {
                "0": {
                    "Metaphor": "abstract is concrete"
                }
            }
        }
        self.assertEqual(2, get_num_attribute_occurances(i1, ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'], 'Metaphor', 'certain is firm'))



    def test_get_total_occurances(self):
        i1 = build_json('test-annotation-1.anvil')
        self.assertEqual(1, get_num_attribute_occurances(i1, ['Metaphor.Type1', 'Metaphor.Type2', 'Metaphor.Type3'], 'Metaphor', 'certain is firm'))


    ## TODO create a real file with more than one instance
if __name__ == '__main__':
    unittest.main()
