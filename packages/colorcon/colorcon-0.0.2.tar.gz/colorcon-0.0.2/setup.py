from distutils.core import (
    setup,
    Extension,
)
from sys import platform as PLATFORM
from typing import List
from colorcon import (__version__, __name__ as __NAME__)

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

AUTHOR = 'Arman Ahmadi'
AUTHOR_EMAIL = 'armanagha6@gmail.com'
setup(name=__NAME__,
      version=__version__,
      description='Colored your text',
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      long_description='Not defined!',
      packages=['colorcon'],
      package_data={'colorcon': ['*']},
      ext_modules=[_COLORED])
