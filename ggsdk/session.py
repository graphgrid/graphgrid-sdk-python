import typing
from dataclasses import dataclass

import ggcore.session


class ModuleSession():
    # module_name: typing.AnyStr
    def __init__(self,access_key=None, secret_key=None):

        # Create new default session core
        self._session_core = ggcore.session.get_session();

        if access_key or secret_key:
            self._session_core.set_credentials(access_key, secret_key, )


    def module(self, module_name):
        """

        :param module_name:
        :return:
        """
