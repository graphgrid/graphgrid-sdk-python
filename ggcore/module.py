from dataclasses import dataclass


@dataclass
class GraphGridModuleSession:
    def is_available(self):
        pass


class ConfigModuleSession(GraphGridModuleSession):
    def __init__(self, ):
        print("CONFIG SDK MODULE CREATED")


class NlpModuleSession(GraphGridModuleSession):
    def __init__(self, ):
        print("NLP SDK MODULE CREATED")


class SecurityModuleSession(GraphGridModuleSession):
    def __init__(self, ):
        print("SECURITY SDK MODULE CREATED")
