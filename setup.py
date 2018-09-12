# -*- coding: utf8 -*-
from setuptools import setup, find_packages

setup(
    name="StationTool",
    version="0.0.1",
    python_requires='>3.6.0',
    author="Ilmo Salmenperä",
    author_email="ilmo.salmenpera@helsinki.fi",
    packages=find_packages(),
    include_package_data=True,
    url="http://github.com/MrCubanfrog/StationTool",
    license="LICENSE",
    description=(   "Library for handling a seismic station database based on the"
                    "CSS format"),
    install_requires=[
        "nordb",
        "pyproj"
    ],
    long_description=open("README.md").read(),
)
