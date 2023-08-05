''' freemt __init__.py '''
# import sys
# from pathlib import Path
# import importlib

from .switch_to import switch_to  # noqa: F401
from .arun import arun  # noqa: F401
from .make_url import make_url  # noqa: F401
from .httpx_get import httpx_get  # noqa: F401
from .save_tempfile import save_tempfile  # noqa: F401
from .save_tempfile import save_tempfile as open_in_browser # noqa: F401
from .logger_level import logger_level  # noqa: F401
from .mtok import mtok, mdetok  # noqa: F401
from .cos_matrix2 import cos_matrix2  # noqa: F401
from .with_func_attrs import with_func_attrs  # noqa: F401
from .report_time import report_time  # noqa: F401
from .langcode_to_tmxcode import langcode_to_tmxcode  # noqa: F401
from .spiiner import Spinner  # noqa: F401


# sys.path.insert(0, '..')

# __file__ = '__init__.py'
_ = '''
for elm in Path(__file__).parent.glob('*.py'):
    stem = elm.stem
    _ = importlib.import_module(stem, package='freemt_utils')
    globals().update({stem: getattr(_, stem)})
# '''

# version__ = '0.0.1'
# date__ = '2020.2.12'
# version__ = '0.0.4'
# version__ = '0.0.5'
# version__ = '0.0.6'
# version__ = '0.0.7'
__version__ = '0.0.9'
VERSION = tuple(__version__.split('.'))
