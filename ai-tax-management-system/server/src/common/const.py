from enum import Enum

class ResponseStatus(str, Enum):
    Success = "Success"
    Failed = "Failed"
    Error = "Error"

class Environment(str, Enum):
    Development = "development"
    Production = "production"