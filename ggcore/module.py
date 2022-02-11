from dataclasses import dataclass


@dataclass
class ModuleClient:
    def is_available(self):
        pass


class ConfigClient(ModuleClient):
    def __init__(self, ):
        print("CONFIG SDK MODULE CREATED")


class NlpClient(ModuleClient):
    def __init__(self, ):
        print("NLP SDK MODULE CREATED")


class SecurityClient(ModuleClient):
    def __init__(self, ):
        print("SECURITY SDK MODULE CREATED")
