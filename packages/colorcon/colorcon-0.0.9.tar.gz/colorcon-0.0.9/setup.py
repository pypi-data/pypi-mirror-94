from setuptools import (
    setup
)
from pathlib import Path
from colorcon import _infs

AUTHOR = _infs.__author__
AUTHOR_EMAIL = _infs.__author_email__

README = Path('README.md').read_text()

setup(name='colorcon',
      version=_infs.__version__,
      description='Colored your text',
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      long_description=README,
      long_description_content_type='text/markdown',
      packages=['colorcon'],
      package_data={'colorcon': ['*']})
