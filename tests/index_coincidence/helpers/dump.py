"""Generate an example file for use in testing for a specified test binary file."""

import json
import sys

from index_coincidence.main import compute_width_scores

OUTPUT_FILE = "examples.json"

if __name__ == "__main__":
    filename = sys.argv[1]
    print(filename)
    with open(filename, "rb") as f:
        data = f.read()

    assert filename.endswith(".enc")

    expected_width = int(filename[-7:-4])
    scores = compute_width_scores(data)

    try:
        with open(OUTPUT_FILE, "r") as f:
            structure = json.load(f)
    except:
        structure = []

    structure.append((expected_width, scores))

    with open(OUTPUT_FILE, "w") as f:
        f.write(json.dumps(structure))
