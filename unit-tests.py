import unittest
from countmetaphors import *

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

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

if __name__ == '__main__':
    unittest.main()
