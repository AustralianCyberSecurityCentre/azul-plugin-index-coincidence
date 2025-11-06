import unittest

from azul_plugin_index_coincidence import entropy

TEST_BLOCK_SIZE = 256
TEST_BLOCK_COUNT = 100


class EntropiesTest(unittest.TestCase):
    def assertAllAlmostEqual(self, first, second, places=7, msg=None):
        self.assertEqual(len(first), len(second), msg)
        self.assertEqual([round(x - y, places) for x, y in zip(first, second)], [0.0] * len(first), msg)

    def test_eights(self):
        buf = bytes(bytearray([x for x in range(TEST_BLOCK_SIZE)] * TEST_BLOCK_COUNT))

        ent = entropy.block_entropies(buf, TEST_BLOCK_SIZE)
        self.assertAllAlmostEqual(ent[0], [8.0] * TEST_BLOCK_COUNT)
        self.assertEqual(ent[1:], [TEST_BLOCK_SIZE, TEST_BLOCK_COUNT])

        ent = entropy.count_entropies(buf, TEST_BLOCK_COUNT)
        self.assertAllAlmostEqual(ent[0], [8.0] * TEST_BLOCK_COUNT)
        self.assertEqual(ent[1:], [TEST_BLOCK_SIZE, TEST_BLOCK_COUNT])

    def test_zero(self):
        buf = bytes(bytearray([0x41] * TEST_BLOCK_SIZE * TEST_BLOCK_COUNT))

        ent = entropy.block_entropies(buf, TEST_BLOCK_SIZE)
        self.assertAllAlmostEqual(ent[0], [0.0] * TEST_BLOCK_COUNT)
        self.assertEqual(ent[1:], [TEST_BLOCK_SIZE, TEST_BLOCK_COUNT])

        ent = entropy.count_entropies(buf, TEST_BLOCK_COUNT)
        self.assertAllAlmostEqual(ent[0], [0.0] * TEST_BLOCK_COUNT)
        self.assertEqual(ent[1:], [TEST_BLOCK_SIZE, TEST_BLOCK_COUNT])

    def test_nothing(self):
        ent = entropy.block_entropies("", 0)
        self.assertEqual(ent, [[], 0, 0])

        ent = entropy.count_entropies("", 0)
        self.assertEqual(ent, [[], 0, 0])

    def test_minimum_size(self):
        buf = bytes(bytearray([x for x in range(TEST_BLOCK_SIZE)] * TEST_BLOCK_COUNT))

        ent = entropy.block_entropies(buf, 0)
        self.assertGreater(ent[2], 0)
        self.assertLessEqual(ent[1], len(buf))
        self.assertAllAlmostEqual(ent[0], [8.0] * ent[2])

        ent = entropy.count_entropies(buf, 0)
        self.assertGreater(ent[2], 0)
        self.assertLessEqual(ent[1], len(buf))
        self.assertAllAlmostEqual(ent[0], [8.0] * ent[2])
