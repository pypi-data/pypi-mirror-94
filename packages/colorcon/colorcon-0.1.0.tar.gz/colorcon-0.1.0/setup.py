from setuptools import (
    setup
)
from pathlib import Path

__author__ = 'Arman Ahmadi'
__author_email__ = 'armanagha6@gmail.com'

__version_info__ = (0, 1, 0)
__version__ = '{0}.{1}.{2}'.format(*__version_info__)

AUTHOR = __author__
AUTHOR_EMAIL = __author_email__

README = Path('README.md').read_text()

setup(name='colorcon',
      version=__version__,
      description='Colored your text',
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      long_description=README,
      long_description_content_type='text/markdown',
      packages=['colorcon'],
      package_data={'colorcon': ['*']})
