"""Calculate shannon entropy over data."""

from _entropy import block_entropies, count_entropies, entropy


def block_entropies_file(filepath, block_size):
    """Return a list of entropies for given file, with block_size length."""
    with open(filepath, "rb") as fh:
        buf = fh.read()

    return block_entropies(buf, block_size)


def count_entropies_file(filepath, block_count):
    """Return a list of length block_count of entropies for given file."""
    with open(filepath, "rb") as fh:
        buf = fh.read()

    return count_entropies(buf, block_count)


def entropy_file(filepath):
    """Calculate the entropy of a given file."""
    with open(filepath, "rb") as fh:
        buf = fh.read()

    return entropy(buf)
