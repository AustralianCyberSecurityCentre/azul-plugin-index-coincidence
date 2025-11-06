"""Index of coincidence analysis library and command-line."""

import argparse

# Index of coincidence must increase by at least this factor in order to be a possible key width.
# Factors will likely be quite large, often a factor of 20 or more.
MINIMUM_IMPROVEMENT_RATIO = 2.0

# Key width must also exceed this fraction of the best possible widths score.
# Structured underlying data can sometimes result in overall higher index of coincidence scores,
# so this threshold will helps exclude widths that do result in a large increase to the index of coincidence,
# but where that increase is much lower than for other widths
SIGNIFICANT_SCORE_RATIO = 0.333333333

# Maximum width size for computing index of coincidence
MAXIMUM_WIDTH = 300


def index_of_coincidence(d1, d2):
    """Return probability d1 and d2 share the same byte value at any position."""
    return sum(1 for i in range(len(d1)) if d1[i] == d2[i]) / len(d1)


def compute_width_scores(data):
    """Compute the index of coincidence for the given data.

    Key widths are tested up to MAXIMUM_WIDTH.
    Choose possible key widths based on the resulting scores.
    """
    # Compute the index of coincidence for a range of key widths.
    scores = []
    for width in range(1, MAXIMUM_WIDTH + 1):
        # Stop if the width grows to the length of the data.
        if width >= len(data):
            break

        # Compute the index of coincidence of the data with itself after
        # shifting it along by the current key width.
        score = index_of_coincidence(data[:-width], data[width:])
        scores.append((width, score))

    return scores


def filter_width_scores(scores):
    """From a list of widths and scores, select the "valid" widths.

    Choose widths with an index of coincidence that is much higher than the index of coincidence of the baseline
    (the file data as a whole), Exclude widths that are multiples of widths that have already been chosen.
    """
    # Build a cutoff based on soame multiple of the width 1 score.
    baseline = scores[0][1]
    minimum_ioc = MINIMUM_IMPROVEMENT_RATIO * baseline

    # Build another cutoff based on a fraction of the best score.
    best_score = max(score for _, score in scores)
    threshold_score = best_score * SIGNIFICANT_SCORE_RATIO

    # Pick highest cutoff as the threshold. Have 1/256 as another threshold in case index of coincidence of data is 0.
    threshold_score = max(minimum_ioc, threshold_score, 1 / 256)

    possible_widths = []
    for width, score in scores:
        # Ignore any scores which don't meet threshold.
        if score < threshold_score:
            continue

        # Ignore multiples of widths that have already been chosen.
        if any([width % existing == 0 for existing, _ in possible_widths]):
            continue

        possible_widths.append((width, score))
    return possible_widths


def get_features(data):
    """Estimate obfuscation key width on data, using index of coincidence.

    Return an array of width/score tuples, as well as the base index of
    coincidence score of the data, to be used as a baseline.
    """
    # Compute index of coincidence scores for widths up to MAXIMUM_WIDTH.
    scores = compute_width_scores(data)

    # The first entry (for width 1) is the plain index of coincidence for this
    # file.
    baseline = scores[0][1]

    # Filter out low scoring / spurious widths.
    widths = filter_width_scores(scores)

    # Return an array of width/score tuples, and the baseline score.
    return widths, baseline


def main():
    """Calculate and display the index of coincidence on the supplied file."""
    # Use argparse to provide a user interface and collect arguments.
    description = "Compute index of coincidence and find obfuscation widths."
    parser = argparse.ArgumentParser(description=description)

    # Only required argument is a file to scan.
    parser.add_argument("filepath", help="File to analyse.")
    args = parser.parse_args()

    # Load in file data.
    with open(args.filepath, "rb") as f:
        file_data = f.read()

    # Compute baseline index of coincidence and possible widths.
    widths, baseline = get_features(file_data)

    # Display results.
    print("Index of coincidence: %s" % baseline)
    if widths:
        print("Widths:")
        for width, score in widths:
            print("\tWidth %d raises index to %s" % (width, score))


if __name__ == "__main__":
    main()
