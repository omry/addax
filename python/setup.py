"""
Elk python setup.py
"""
import setuptools.command.build_py

from setup import PylintCommand, ANTLRCommand

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setuptools.setup(
        cmdclass={
            'pylint': PylintCommand,
            'antlr': ANTLRCommand,
        },
        name="elk",
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
        packages=['elk'],
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'antlr4-python3-runtime;python_version>="3.0"',
            'antlr4-python2-runtime;python_version<"3.0"',
        ]
    )
