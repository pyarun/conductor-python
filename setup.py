import setuptools
import os

version = os.environ.get("CONDUCTOR_PYTHON_VERSION")
if version is None:
    version = '1.1.10-SIMPLIFIED'

setuptools.setup(
    version=version,
)
