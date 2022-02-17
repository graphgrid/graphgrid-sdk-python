import ggcore.client_factory
from ggcore.client import GraphGridModuleClient
from ggsdk.session import GraphGridSession



class SdkMain:

    _session: GraphGridSession

    def __init__(self, session):
        self._session = session
        # get bootstrap config

        # Get config client

        # Get security client
            # Get url base, setup

    def get_client(self, name) -> GraphGridModuleClient:
        return ggcore.client_factory.client(name) # should session be passed in here too? the client should keep track of the session itself?
