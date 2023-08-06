from setuptools import (
    setup,
    Extension,
)
from sys import platform as PLATFORM
from typing import List
from pathlib import Path
from colorcon import _infs

AUTHOR = _infs.__author__
AUTHOR_EMAIL = _infs.__author_email__

README = Path('README.md').read_text()

extraLinkArgs: List[str] = []
extraCompileArgs: List[str] = []

if PLATFORM == 'win32':
    # On windows platform(known as win32)
    # - install mingw
    # - add it to system path(/bin folder in mingw path) !important
    # - call with setup.py build -c mingw32
    import distutils.cygwinccompiler as _CYGWIN
    import distutils.msvccompiler as _MSVC

    _CYGWIN.get_msvcr = lambda: []
    _MSVC.get_msvcr = lambda: []

    extraLinkArgs += ['-static', "-Wl,-Bstatic", "-lpthread"]
    extraCompileArgs += ['-lkernel32']

_COLORED = Extension('_colored',
                     sources=['colored.cpp'],
                     extra_compile_args=extraCompileArgs,
                     extra_link_args=extraLinkArgs,
                     language="c++")

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
