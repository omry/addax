#!/usr/bin/env python

import distutils.cmd
import distutils.log
import os
import subprocess
import sys
import re
import setuptools.command.build_py
import shutil
from os import path

"""
Addax setup
    Instructions:
    # Build:
    rm -rf dist/ addax.egg-info/
    python3 setup.py sdist bdist_wheel
    # Upload:
    python3 -m twine upload dist/*
"""


class ANTLRCommand(distutils.cmd.Command):
    """Generate parsers using ANTLR."""

    description = 'Run ANTLR'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run command."""
        root_dir = path.dirname(path.realpath(__file__))
        for pyver in (2, 3):
            command = [sys.executable,
                       path.join(root_dir, 'bin/antlr4.py'),
                       '-Dlanguage=Python{}'.format(pyver),
                       '-o',
                       'addax/gen{}'.format(pyver),
                       '-Xexact-output-dir',
                       path.join(root_dir, 'grammar/YAML.g4')]
            self.announce('Generating parser for Python {}: {}'.format(pyver, command), level=distutils.log.INFO)
            subprocess.check_call(command)


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        if not self.dry_run:
            self.run_command('antlr')
        setuptools.command.build_py.build_py.run(self)


class CleanCommand(distutils.cmd.Command):
    """
    Our custom command to clean out junk files.
    """
    description = "Cleans out junk files we don't want in the repo"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def find(self, root, pattern):
        res = []
        for parent, dirs, files in os.walk(root):
            for f in dirs + files:
                if re.findall(pattern, f):
                    res.append(path.join(parent, f))
        return res

    def run(self):
        deletion_list = [
            '.coverage',
            '.eggs',
            '.tox',
            '.pytest_cache',
            'addax.egg-info',
            'build',
        ]
        for p in ['__pycache__', re.escape('.pyc')]:
            deletion_list.extend(self.find('.', p))
        for gen in ['addax/gen2', 'addax/gen3']:
            deletion_list.extend(self.find(gen, 'YAML.*'))

        for f in deletion_list:
            if path.exists(f):
                if path.isdir(f):
                    shutil.rmtree(f, ignore_errors=True)
                else:
                    os.unlink(f)


with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setuptools.setup(
        cmdclass={
            'antlr': ANTLRCommand,
            'clean_all': CleanCommand,
            'build_py': BuildPyCommand,
        },
        name="addax",
        version="0.1",
        author="Omry Yadan",
        author_email="omry@yadan.net",
        description="YAML to AST parser",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        url="https://github.com/omry/addax",
        keywords='yaml parser',
        packages=['addax'],
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'antlr4-python3-runtime;python_version>="3.0"',
            'antlr4-python2-runtime;python_version<"3.0"',
        ]
    )
