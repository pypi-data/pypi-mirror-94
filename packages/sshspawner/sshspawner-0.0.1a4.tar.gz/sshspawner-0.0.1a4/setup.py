#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) Juptyer Development Team.
# Distributed under the terms of the Modified BSD License.
#
# ----------------------------------------------------------------------------
# Minimal Python version sanity check (from IPython/Jupyterhub)
# ----------------------------------------------------------------------------
import os
from setuptools import setup, find_packages

cur_dir = os.path.abspath(os.path.dirname(__file__))


def read(path):
    with open(path, "r") as _file:
        return _file.read()


def read_req(name):
    path = os.path.join(cur_dir, name)
    return [req.strip() for req in read(path).splitlines() if req.strip()]


version_ns = {}
with open(os.path.join(cur_dir, "version.py")) as f:
    exec(f.read(), {}, version_ns)


long_description = open("README.rst").read()
setup(
    name="sshspawner",
    version=version_ns["__version__"],
    description="""SSH Spawner: A custom spawner for Jupyterhub to spawn
                   notebooks over SSH""",
    long_description=long_description,
    author="Rasmus Munk",
    author_email="munk1@live.dk",
    packages=find_packages(),
    url="https://github.com/rasmunk/sshspawner.git",
    license="BSD",
    platforms="Linux, Mac OS X",
    keywords=["Interactive", "Interpreter", "Shell", "Web", "JupyterHub", "Spawner"],
    install_requires=read_req("requirements.txt"),
    extras_require={
        "test": read_req("requirements-test.txt"),
        "dev": read_req("requirements-dev.txt"),
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
