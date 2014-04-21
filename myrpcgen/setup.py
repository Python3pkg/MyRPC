#!python

from distutils.core import setup
import sys

sys.path.append("../etc")
from distutils_helper import create_config

# Run setup.

config = create_config("../README.md", {"name": "myrpcgen",
                                        "description": "MyRPC code generator tool",
                                        "scripts": ("src/myrpcgen",),
                                        "package_dir": {"myrpcgen": "src/lib"},
                                        "packages": ("myrpcgen",)})

setup(**config)
