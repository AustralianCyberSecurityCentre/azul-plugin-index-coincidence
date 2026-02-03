import unittest

from azul_runner import FV, Event, JobResult, State, test_template

from azul_plugin_index_coincidence.main import AzulPluginIndexCoincidence


class TestIndexCoincidence(test_template.TestPlugin):
    PLUGIN_TO_TEST = AzulPluginIndexCoincidence

    def test_low_entropy(self):
        """
        Test that no features are produced for low entropy files.
        """
        low_entropy_data = b"\x00" * 1024
        result = self.do_execution(data_in=[("content", low_entropy_data)])
        self.assertJobResult(result, JobResult(state=State(State.Label.OPT_OUT)))

    def test_no_widths(self):
        """
        Test high entropy data with no widths don't produce any.
        """
        data = bytes(list(range(256)))
        result = self.do_execution(data_in=[("content", data)])
        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="40aff2e9d2d8922e47afd4648e6967497158785fbd1da870e7110266bf944880",
                        features={"index_of_coincidence": [FV(0.0)]},
                    )
                ],
            ),
        )

    def test_widths(self):
        """
        Test high entropy data with a width produces features.
        """
        data = bytes(list(range(256))) * 2
        result = self.do_execution(data_in=[("content", data)])
        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        entity_type="binary",
                        entity_id="110009dcee21620b166f3abfecb5eff7a873be729d1c2d53822e7acc5f34eb9b",
                        features={
                            "index_of_coincidence": [FV(0.0)],
                            "index_of_coincidence_width": [FV(256, label="1.0")],
                        },
                    )
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
