
"""
    " =========================================================
    "   Sorted by      name
    "   Sort sequence: [\\/]$,\\<core\\%(\\.\\d\\+\\)\\=\\>,\\.h$,\\.c$,
    " \\.cpp$,\\~\\=\\*$,*,\\.o$,\\.obj$,\\.info$

    "   Quick Help: <F1>:help  -:go up dir  D:delete
    "   R:rename  s:sort-by  x:special

"""

# This is a module that contains a find_version function
# which automatically

# seeks, finds and returns the version of the package.
# The version of the package must be in the __init__.py file
# of the main directory
# the version must be a string attributed to a variable
# named __version__.

import os
import re
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")
