from ggcore.utils import CONFIG, SECURITY, NLP


class GraphGridModuleClient:
    """
    url_base: address of client (ex. "localhost", "gg-dev")
    client_name: subclass defined; static name of the client
    """
    _url_base: str
    _client_name: str

    def is_available(self):
        pass

    def client_name(self):
        pass

    def url_base(self):
        pass

    def _http_base(self):
        return f'{self.url_base}/1.0/{self.client_name}/'


class ConfigClient(GraphGridModuleClient):
    _client_name = CONFIG

    @property
    def client_name(self):
        return self._client_name

    @property
    def url_base(self):
        return self._url_base



    def get_data(self, path: str) -> str:
        """
        """
        # trigger_response = requests.post(
        #     f'{self.url}/api/v1/dags/{dag_id}/dagRuns',
        #     json={"conf": request_body, "execution_date": execution_date},
        #     headers=HEADERS)
        # if trigger_response.status_code != 200:
        #     raise RuntimeError(f'DAG {dag_id} could not be triggered. Response: "{trigger_response.text}"')
        # dag_run_id = json.loads(trigger_response.text)["dag_run_id"]
        # return dag_run_id


class SecurityClient(GraphGridModuleClient):
    _client_name = SECURITY

    @property
    def client_name(self):
        return self._client_name

    @property
    def url_base(self):
        return self._url_base


class NlpClient(GraphGridModuleClient):
    _client_name = NLP

    @property
    def client_name(self):
        return self._client_name

    @property
    def url_base(self):
        return self._url_base
