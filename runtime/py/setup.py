#!python

from distutils.core import setup
import sys

sys.path.append("../../etc")
from distutils_helper import create_config

# Run setup.

config = create_config("../../README.md", {"name": "myrpc-runtime",
                                           "description": "MyRPC Python runtime",
                                           "package_dir": {"myrpc": "src"},
                                           "packages": ("myrpc",
                                                        "myrpc.codec",
                                                        "myrpc.transport",
                                                        "myrpc.util")})

setup(**config)
