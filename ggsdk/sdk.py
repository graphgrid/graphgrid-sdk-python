import ggcore.client_factory
from ggsdk.session import GraphGridSession


class SdkMain:

    _session: GraphGridSession

    def __init__(self, session):
        self._session = session
        # get bootstrap config

        # Get config client

        # Get security client
            # Get url base, setup


        _nlp_client = ggcore.client_factory.client("nlp") # this seems wrong

    def save(self):
        pass

    def train(self):
        pass

    def get_job_status(self):
        pass

    def get_job_results(self):
        pass