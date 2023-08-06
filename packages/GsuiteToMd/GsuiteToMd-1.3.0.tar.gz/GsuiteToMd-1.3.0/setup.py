import sys

import setuptools
from setuptools import setup
from version import get_git_version

# Extra dependecies to run tests
tests_requirements = [
    "pytest>=4.6.0",
    "timeout-decorator",
    "funcy>=1.14",
    "flake8",
    "flake8-docstrings",
]

if sys.version_info >= (3, 6):
    tests_requirements.append("black==19.10b0")

setup(
    name="GsuiteToMd",
    version=get_git_version(),
    author="Laurent Maumet",
    author_email="laurent@aurora-5r.fr",
    packages=setuptools.find_packages(),
    url="https://github.com/aurora-5r/GsuiteToMd",
    description="Tools to convert gsuite Documents to markdown.",
    long_description=open("README.rst").read(),
    install_requires=[
        "google-api-python-client >= 1.12.5",
        "PyYAML >= 3.0",
        "bs4",
        "pydrive",
        "markdownify",
        "argparse",
        "lxml"
    ],
    extras_require={"tests": tests_requirements},
)
