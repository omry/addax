import sys

try:
    if sys.version_info >= (3, 0):
        from .gen3 import YAMLListener
        from .gen3 import YAMLLexer
        from .gen3 import YAMLParser
    else:
        from .gen2 import YAMLListener
        from .gen2 import YAMLLexer
        from .gen2 import YAMLParser
except ImportError as err:
    raise ImportError("Error importing generated parser, run setup.py antlr to generate")
from .antelope import Antelope