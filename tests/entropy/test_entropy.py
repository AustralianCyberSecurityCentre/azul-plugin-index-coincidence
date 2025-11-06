import unittest
from math import log
from random import randrange

from azul_plugin_index_coincidence import entropy

TEST_BUF_LEN = 256


class EntropyTest(unittest.TestCase):
    def test_eight(self):
        buf = bytes(bytearray([x for x in range(TEST_BUF_LEN)]))
        ent = entropy.entropy(buf)
        self.assertAlmostEqual(ent, 8.0)

    def test_zero(self):
        buf = bytes(bytearray([0x41]) * TEST_BUF_LEN)
        ent = entropy.entropy(buf)
        self.assertAlmostEqual(ent, 0.0)

    def test_nothing(self):
        ent = entropy.entropy("")
        self.assertEqual(ent, 0.0)

    def test_random(self):
        # this will generate something of an entropy close to
        # (but very likely not) 8.0
        buf = bytes(bytearray([randrange(0, 256) for _ in range(TEST_BUF_LEN)]))

        # independant calculation of entropy
        bins = [0] * 256
        for x in buf:
            # python3 will get a byte/int back for each element, whereas
            # python2 will get a string which can't index into a list. hence,
            # handle the exception.
            try:
                bins[x] += 1
            except TypeError:
                bins[ord(x)] += 1
        pr = [float(x) / TEST_BUF_LEN for x in bins]
        ent_baseline = -1 * sum(x * log(x, 2) if x > 0 else 0.0 for x in pr)

        # library calculation
        ent = entropy.entropy(buf)
        self.assertAlmostEqual(ent, ent_baseline)

    def test_kwargs(self):
        buf = bytes(bytearray([x for x in range(TEST_BUF_LEN)]))
        ent = entropy.entropy(buf=buf)
        self.assertAlmostEqual(ent, 8.0)
