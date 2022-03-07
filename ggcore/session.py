"""

User does not interact with this session obj, instead the SessionCore is meant to hold state information about the current sdk

"""

class SdkSession:
    is_authenticated_for_basic: bool
    is_authenticated_for_bearer: bool

