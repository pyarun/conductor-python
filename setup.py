import setuptools
import os

version = os.environ.get('CONDUCTOR_PYTHON_VERSION', "1.1.7")
if version is None:
    version = '0.0.0-SNAPSHOT'

setuptools.setup(
    version=version,
)
