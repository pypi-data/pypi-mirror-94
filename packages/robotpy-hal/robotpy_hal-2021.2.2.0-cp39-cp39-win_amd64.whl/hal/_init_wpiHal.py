# This file is automatically generated, DO NOT EDIT
# fmt: off

from os.path import abspath, join, dirname, exists
_root = abspath(dirname(__file__))

# runtime dependencies
import wpiutil._init_wpiutil
from ctypes import cdll

try:
    _lib = cdll.LoadLibrary(join(_root, "lib", "wpiHal.dll"))
except FileNotFoundError:
    if not exists(join(_root, "lib", "wpiHal.dll")):
        raise FileNotFoundError("wpiHal.dll was not found on your system. Is this package correctly installed?")
    raise Exception("wpiHal.dll could not be loaded. Do you have Visual Studio C++ Redistributible 2019 installed?")

