"""Find index-of-coincidence widths to find obfuscation key widths and data repetition."""

from azul_runner import FV, BinaryPlugin, Feature, Job, State, add_settings, cmdline_run

from .entropy import entropy
from .index_coincidence.main import get_features


class AzulPluginIndexCoincidence(BinaryPlugin):
    """Find index-of-coincidence widths to find obfuscation key widths and data repetition."""

    CONTACT = "ASD's ACSC"
    VERSION = "2025.03.18"
    # FUTURE: enable dispatcher to filter binaries of interest on 'entrpy'
    # This would allow us to filter input for this plugin to entropy value range/min
    #
    # Feature the index of coincidence for a file.
    # If this index improves by assuming the file is obfuscated by a key with a certain width,
    # feature those widths and their improved index.
    FEATURES = [
        Feature(
            "index_of_coincidence",
            "Probability that two randomly selected bytes have the same value",
            float,
        ),
        Feature(
            "index_of_coincidence_width",
            "Possible key widths which improve the index of coincidence",
            int,
        ),
    ]
    SETTINGS = add_settings(
        filter_max_content_size=(int, 5 * 1024 * 1024),
        filter_data_types={"content": []},
    )

    def execute(self, job: Job):
        """Run across data for any file type.

        Low entropy files will be opted-out.
        """
        # Read in the sample data.
        data = job.get_data().read()

        # Only want to run on high entropy files.
        # The value of this plugin is when it finds widths, and the nature of those files
        # means they will have very high entropy.
        if entropy(data) < 6.0:
            return State.Label.OPT_OUT

        # Use the index_coincidence package to compute the results.
        widths, baseline = get_features(data)
        self.add_feature_values("index_of_coincidence", baseline)

        for width, improved_index in widths:
            # The width is the feature, and has a label with the improved index of coincidence score.
            self.add_feature_values("index_of_coincidence_width", FV(width, label=str(improved_index)))


def main():
    """Run plugin via command-line."""
    cmdline_run(plugin=AzulPluginIndexCoincidence)


if __name__ == "__main__":
    main()
