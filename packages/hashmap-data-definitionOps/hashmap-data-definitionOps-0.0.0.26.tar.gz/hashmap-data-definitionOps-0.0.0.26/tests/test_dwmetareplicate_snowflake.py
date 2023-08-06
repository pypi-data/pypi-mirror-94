import os
from hm_datadefinitionops import __version__


def test_version():
    print(f"--> Current dir : {os.getcwd()} ")
    assert __version__ == "0.0.1b"
