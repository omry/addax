#!/usr/bin/env python

import distutils.cmd
import distutils.log
import os
import sys
from distutils import dir_util
from os.path import *

import re
import setuptools.command.build_py
import setuptools.command.sdist
import shutil
import subprocess

"""
Addax setup
    Instructions:
    # build
    python setup.py clean_all sdist bdist_wheel
    # upload
    python3 -m twine upload dist/*
    # clean
    python setup.py clean_all
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
        root_dir = dirname(realpath(__file__))
        try:
            """
            This is a nasty hack to work around setuptools inability to handle copying files from the parent dir.
            When we build we copy the parent grammar and bin directories here.
            And we use them.
            In addition, when we create the source dist (sdist) tox is using, we add those same into it - 
            because this is what the tox build is getting access to.
            finally, this code need to work both in the tox mode where bin and grammar are in
            the source tree and in normal mode when they are not, so it copies them here only if 
            they are not already here and finally deletes them.
            """
            copied_bin = False
            copied_grammar = False
            if not exists('bin'):
                dir_util.copy_tree('../bin', 'bin')
                copied_bin = True
            if not exists('grammar'):
                dir_util.copy_tree('../grammar', 'grammar')
                copied_grammar = True

            for pyver in (2, 3):
                command = [sys.executable,
                           join(root_dir, 'bin/antlr4.py'),
                           '-Dlanguage=Python{}'.format(pyver),
                           '-o',
                           'addax/gen{}'.format(pyver),
                           '-Xexact-output-dir',
                           join(root_dir, 'grammar/YAML.g4')]
                self.announce('Generating parser for Python {}: {}'.format(pyver, command), level=distutils.log.INFO)
                subprocess.check_call(command)
        finally:
            if copied_bin:
                shutil.rmtree('bin', ignore_errors=True)
            if copied_grammar:
                shutil.rmtree('grammaer', ignore_errors=True)


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        if not self.dry_run:
            self.run_command('antlr')
        setuptools.command.build_py.build_py.run(self)


class SDistCommand(setuptools.command.sdist.sdist):
    """Custom build command."""

    def run(self):
        super(SDistCommand, self).run()

    def make_release_tree(self, base_dir, files):
        super(SDistCommand, self).make_release_tree(base_dir, files)
        # sdist can't handle files outside of the root dir of the build.
        # a little hack to help it.
        self.copy_tree("../bin", join(base_dir, 'bin'))
        self.copy_tree("../grammar", join(base_dir, 'grammar'))


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
                    res.append(join(parent, f))
        return res

    def run(self):
        deletion_list = [
            '.coverage',
            '.eggs',
            '.tox',
            '.pytest_cache',
            'addax.egg-info',
            'build',
            'dist',
            # copied by antlr command hack
            'bin',
            'grammar',
        ]
        for p in ['__pycache__', re.escape('.pyc')]:
            deletion_list.extend(self.find('.', p))
        for gen in ['addax/gen2', 'addax/gen3']:
            deletion_list.extend(self.find(gen, 'YAML.*'))

        for f in deletion_list:
            if exists(f):
                if isdir(f):
                    shutil.rmtree(f, ignore_errors=True)
                else:
                    os.unlink(f)


with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setuptools.setup(
        cmdclass={
            'antlr': ANTLRCommand,
            'clean_all': CleanCommand,
            'sdist': SDistCommand,
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
        ],
        # Install development dependencies with 
        # pip install -e .[dev]
        extras_require={
            'dev': [
                'pytest',
                'tox',
                'coveralls'
            ]
        }

    )
