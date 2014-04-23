#!python

from distutils.core import setup
from distutils_helper import create_config

# Run setup.

config = create_config({"name": "myrpcgen",
                        "description": "MyRPC code generator tool",
                        "scripts": ("src/myrpcgen",),
                        "package_dir": {"myrpcgen": "src/lib"},
                        "packages": ("myrpcgen",)})

setup(**config)
