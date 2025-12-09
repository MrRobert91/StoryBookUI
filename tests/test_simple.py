import sys
import os

def test_environment_setup():
    print(f"Python executable: {sys.executable}")
    print(f"Sys path: {sys.path}")
    import pydantic
    print(f"Pydantic file: {pydantic.__file__}")
    assert True
