#!/usr/bin/env python

import distutils.cmd
import distutils.log
import subprocess

import setuptools.command.build_py


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
        for pyver in (2, 3):
            command = ['antlr4',
                       '-Dlanguage=Python{}'.format(pyver),
                       '-o',
                       'yamelk/gen{}'.format(pyver),
                       '-Xexact-output-dir',
                       'grammar/YAML.g4']
            self.announce('Generating parser for Python {}: {}'.format(pyver, command), level=distutils.log.INFO)
            subprocess.check_call(command)


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        if not self.dry_run:
            self.run_command('antlr')
        setuptools.command.build_py.build_py.run(self)


with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setuptools.setup(
        cmdclass={
            'antlr': ANTLRCommand,
            'build_py': BuildPyCommand,
        },
        name="yamelk",
        version="0.1",
        author="Omry Yadan",
        author_email="omry@yadan.net",
        description="YAML to AST parser",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        url="https://github.com/omry/elk",
        keywords='yaml parser',
        packages=['yamelk'],
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
