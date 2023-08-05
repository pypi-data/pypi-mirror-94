'''
moses tok detok
'''
# pylint: disable=invalid-name, unused-import

import sys

try:
    import sacremoses  # noqa: F401
except ModuleNotFoundError:
    import subprocess as sp
    import shlex
    proc = sp.Popen(
        shlex.split('pip install sacremoses'), stdout=-1, stderr=-1)
    out, err = proc.communicate()
    if err:
        sys.stderr.write('error: %s' % err.decode())
    sys.stdout.write('%s' % out.decode())

from sacremoses import MosesTokenizer, MosesDetokenizer

MTOK = MosesTokenizer().tokenize
MDETOK = MosesDetokenizer().detokenize
mtok = MTOK
mdetok = MDETOK
