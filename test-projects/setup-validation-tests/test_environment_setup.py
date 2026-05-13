import sys

def test_python_version_is_supported():
    assert sys.version_info.major == 3
    assert sys.version_info.minor == 11

def test_pytest_environment_is_ready():
    assert True
    