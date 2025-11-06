import json
import os
import unittest

from azul_plugin_index_coincidence.index_coincidence.main import (
    compute_width_scores,
    filter_width_scores,
    get_features,
    index_of_coincidence,
)

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "test_data.json")


class TestIndexCoincidence(unittest.TestCase):
    def test_index_of_coincidence(self):
        """
        Test that index of coincidence is correctly computed.
        """
        # If the bytes in every position are identical, should get an index
        # of coincidence of 1.
        data = bytes(list(range(256)))
        ioc = index_of_coincidence(data, data)
        self.assertAlmostEqual(ioc, 1.0)

        # If no bytes in the same position are identical, should get an
        # index of coincidence of 0.
        ioc = index_of_coincidence(b"\x01\x02\x03", b"\xff\xfe\xfd")
        self.assertAlmostEqual(ioc, 0.0)

        # 50% coincidence.
        ioc = index_of_coincidence(b"\xff\xff\xff\xff", b"\xff\xff\xee\xee")
        self.assertAlmostEqual(ioc, 0.5)

    def test_compute_width_scores(self):
        """
        Test that index of coincidence is correctly computed for various widths.
        """
        # Check a small sample that was easy to do by hand.
        data = b"\x01\x02\x03\x04\x01\x02\x03\x04"
        scores = compute_width_scores(data)
        expected = [(1, 0.0), (2, 0.0), (3, 0.0), (4, 1.0), (5, 0.0), (6, 0.0), (7, 0.0)]
        self.assertEqual(scores, expected)

        # Do a bigger example, but just check that results stp at the correct width.
        data = b"\xff" * 42
        scores = compute_width_scores(data)
        expected = [(i, 1.0) for i in range(1, 42)]
        self.assertEqual(scores, expected)

        # For data with length zero, expect an empty list.
        self.assertEqual(compute_width_scores(b""), [])

    def test_filter_width_scores(self):
        """
        Load a collection of examples from a JSON file, which contains a collection of scores,
        and the expected widths that should be extracted from them.
        """
        with open(TEST_DATA_PATH, "r") as f:
            examples = json.load(f)

        # Verify test data is not empty
        self.assertTrue(len(examples) > 0)

        for expected_width, scores in examples:
            # Filter the list of scores
            filtered = filter_width_scores(scores)

            self.assertEqual(len(filtered), 1)
            self.assertEqual(filtered[0][0], expected_width)

    def test_get_features(self):
        """
        Test the highest level function.
        Verify it returns the expected widths array, and baseline index of coincidence.
        """
        data = b"Some data we can obfuscated and test our code on."
        key = b"\x11\x22\x33\x44"
        enc = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

        widths, baseline = get_features(enc)

        expected_widths = [(4, 1 / 9)]
        self.assertEqual(widths, expected_widths)

        expected_baseline = 0
        self.assertEqual(baseline, expected_baseline)


if __name__ == "__main__":
    unittest.main()
