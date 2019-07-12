"""
ANTLR compiler invocation
"""
import distutils.cmd
import distutils.log
import subprocess
import sys


class ANTLRCommand(distutils.cmd.Command):
    """Generate parsers using ANTLR."""

    description = 'Run antlr'
    user_options = [
        # ('pylint-rcfile=', None, 'path to Pylint config file'),
    ]

    def __init__(self, dist):
        super(ANTLRCommand, self).__init__(dist)
        self.grammar_file = None

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.grammar_file = '../grammar/YAML.g4'

    def finalize_options(self):
        pass

    def run(self):
        """Run command."""
        command = ['antlr4']
        if sys.version_info >= (3, 0):
            command.extend(['-Dlanguage=Python3', '-o', 'elk/gen3'])
        else:
            command.extend(['-Dlanguage=Python2', '-o', 'elk/gen2'])
        command.extend(['-Xexact-output-dir', '../grammar/YAML.g4'])
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)
        subprocess.check_call(command)
