from unittest import TestCase

from ggcore.credentials import Credentials
from ggcore.security_base import SdkAuth
from ggcore.utils import RequestAuthType, AUTH_HEADER_KEY


class TestAuth(TestCase):
    _test_credentials = Credentials(access_key='a3847750f486bd931de26c6e683b1dc4',
                                    secret_key='81a62cea53883f4a163a96355d47656e',
                                    token="d04ce18b-24ba-4a49-b80a-cf3730f36908")

    def test_auth_basic_header(self):
        expected_headers = {
            AUTH_HEADER_KEY: 'Basic YTM4NDc3NTBmNDg2YmQ5MzFkZTI2YzZlNjgzYjFkYzQ6ODFhNjJjZWE1Mzg4M2Y0YTE2M2E5NjM1NWQ0NzY1NmU='}

        actual_headers = SdkAuth(credentials=self._test_credentials).get_auth_for_http(RequestAuthType.BASIC)

        assert actual_headers == expected_headers

    def test_auth_bearer_header(self):
        expected_headers = {AUTH_HEADER_KEY: 'Bearer d04ce18b-24ba-4a49-b80a-cf3730f36908'}

        actual_headers = SdkAuth(credentials=self._test_credentials).get_auth_for_http(RequestAuthType.BEARER)

        assert actual_headers == expected_headers
