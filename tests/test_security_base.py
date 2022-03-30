"""Define tests around the security base and auth header creation."""

from ggcore.security_base import SdkAuthHeaderBuilder
from ggcore.utils import AUTH_HEADER_KEY
from tests.test_base import TestBootstrapBase


class TestAuth(TestBootstrapBase):
    """Test auth header creation."""

    # pylint: disable=line-too-long
    def test_auth_basic_header(self):
        """Test basic auth header creation."""
        expected_headers = {
            AUTH_HEADER_KEY: 'Basic YTM4NDc3NTBmNDg2YmQ5MzFkZTI2YzZlNjgzYjFkYzQ6ODFhNjJjZWE1Mzg4M2Y0YTE2M2E5NjM1NWQ0NzY1NmU='}

        actual_headers = SdkAuthHeaderBuilder.get_basic_header(
            self._test_credentials)

        assert actual_headers == expected_headers

    def test_auth_bearer_header(self):
        """Test bearer auth header creation."""
        expected_headers = {
            AUTH_HEADER_KEY: f'Bearer {TestBootstrapBase.TEST_TOKEN}'}

        actual_headers = SdkAuthHeaderBuilder.get_bearer_header(
            self._test_credentials)

        assert actual_headers == expected_headers
