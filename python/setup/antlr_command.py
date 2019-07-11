"""
ANTLR compiler invocation
"""
import distutils.cmd
import distutils.log
import os
import subprocess


class ANTLRCommand(distutils.cmd.Command):
    """Generate parsers using ANTLR."""

    description = 'Run antlr'
    user_options = [
        # ('pylint-rcfile=', None, 'path to Pylint config file'),
    ]

    def __init__(self):
        super(ANTLRCommand, self).__init__()
        self.grammar_files = None

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.grammar_files = ['../grammaer/YAML.g4']

    def finalize_options(self):
        """Post-process options."""
        if self.grammar_files:
            for file_ in self.grammar_files:
                assert os.path.exists(file_), \
                    'Pylint config file {} does not exist.'.format(self.pylint_rcfile)

    def run(self):
        """Run command."""
        command = ['antlr4']
        command.append(os.getcwd())
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)
        subprocess.check_call(command)
