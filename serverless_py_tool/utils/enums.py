from enum import Enum

class PyVenvManager(str, Enum):
    VENV = "venv"
    PIPENV = "pipenv"


class BuildStrategies(str, Enum):
    ZIP = "zip"
    DOCKER = "docker"
    REFERENCE = "reference"


class IaCTechnologies(str, Enum):
    SAM = "sam"
    CLOUDFORMATION = "cloudformation"
    TERRAFORM = "terraform"

class PythonRuntime(str, Enum):
    PY37 = "python3.7"
    PY38 = "python3.8"
    PY39 = "python3.9"
    PY310 = "python3.10"
    PY311 = "python3.11"
