from dataclasses import dataclass


@dataclass
class GraphGridModule:
    def is_available(self):
        pass


class ConfigModule(GraphGridModule):
    def __init__(self, ):
        print("CONFIG SDK MODULE CREATED")


class NlpModule(GraphGridModule):
    def __init__(self, ):
        print("NLP SDK MODULE CREATED")


class SecurityModule(GraphGridModule):
    def __init__(self, ):
        print("SECURITY SDK MODULE CREATED")
