import setuptools
import os
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version="1.1.11"

setuptools.setup(
    name="conductor-python",
    version=version,
    author="Arun",
    author_email="mittal.talk@gmail.com",
    description="Python client for OSS Conductor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/orkes-io/conductor-python",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.1",
        "urllib3>=1.26.6",
        "python-dateutil>=2.8.2",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    keywords="oss conductor workflow orchestration",
    project_urls={
        "Documentation": "https://conductor-oss.github.io/conductor/index.html",
        "Source": "https://github.com/conductor-oss/python-sdk",
        "Tracker": "https://github.com/conductor-oss/python-sdk/issues",
    },
)
