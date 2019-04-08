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

if __name__ == '__main__':
    unittest.main()
