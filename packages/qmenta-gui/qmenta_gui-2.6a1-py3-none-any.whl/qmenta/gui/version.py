from os import path
from typing import Optional

release: str = '2.5'
revision: Optional[str] = None

revision_filename: str = path.join(path.dirname(__file__), 'REVISION')
try:
    with open(revision_filename) as f:
        revision = ''.join(['dev', f.read().strip()])
except FileNotFoundError:
    pass

__version__: str
if revision:
    __version__ = '.'.join([release, revision])
else:
    __version__ = release

if __name__ == '__main__':
    print(__version__)
