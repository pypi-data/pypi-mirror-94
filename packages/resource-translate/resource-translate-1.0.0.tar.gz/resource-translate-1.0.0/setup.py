from sys import argv

from setuptools import setup


packages = ["resource_translate"]

if "dev" in argv:
    packages.append("tests")

setup(packages=packages)
