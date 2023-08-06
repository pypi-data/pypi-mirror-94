"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="d2apy",
    version="1.0.0",
    description="Dhis2 API wrapper",
    long_description=open("README.md").read(),
    license="GPLv3+",
    url="https://github.com/EyeSeeTea/d2apy.git",
    author="EyeSeeTea",
    author_email="info@eyeseetea.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["d2apy"],
    include_package_data=True,
    install_requires=[
        "jsonobject", "requests"
    ],
)
