import os
import tempfile
import unittest

from azul_plugin_index_coincidence import entropy

TEST_BLOCK_SIZE = 256
TEST_BLOCK_COUNT = 100


class EntropyFilesTest(unittest.TestCase):
    def assertAllAlmostEqual(self, first, second, places=7, msg=None):
        self.assertEqual(len(first), len(second), msg)
        self.assertEqual(
            [round(x - y, places) for x, y in zip(first, second)],
            [0.0] * len(first),
            msg,
        )

    def test_entropy(self):
        buf = bytes(bytearray([int(x) for x in range(TEST_BLOCK_SIZE)]))
        fd = None
        fpath = None
        try:
            fd, fpath = tempfile.mkstemp()
            self.assertEqual(os.write(fd, bytes(buf)), len(buf))

            ent = entropy.entropy_file(fpath)
            self.assertAlmostEqual(ent, 8.0)
        finally:
            if fd:
                os.close(fd)
            if fpath:
                os.unlink(fpath)

    def test_entropies(self):
        buf = bytes(bytearray([0x41]) * TEST_BLOCK_SIZE * TEST_BLOCK_COUNT)

        fd = None
        fpath = None
        try:
            fd, fpath = tempfile.mkstemp()
            self.assertEqual(os.write(fd, buf), len(buf))

            ent = entropy.block_entropies_file(fpath, TEST_BLOCK_SIZE)
            self.assertAllAlmostEqual(ent[0], [0.0] * TEST_BLOCK_COUNT)
            self.assertEqual(ent[1:], [TEST_BLOCK_SIZE, TEST_BLOCK_COUNT])

            ent = entropy.count_entropies_file(fpath, TEST_BLOCK_COUNT)
            self.assertAllAlmostEqual(ent[0], [0.0] * TEST_BLOCK_COUNT)
            self.assertEqual(ent[1:], [TEST_BLOCK_SIZE, TEST_BLOCK_COUNT])
        finally:
            if fd:
                os.close(fd)
            if fpath:
                os.unlink(fpath)
