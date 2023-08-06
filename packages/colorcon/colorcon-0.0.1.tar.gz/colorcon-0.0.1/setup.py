from distutils.core import (
    setup,
    Extension,
)
from sys import platform as PLATFORM
from typing import List

extraLinkArgs: List[str] = []
extraCompileArgs: List[str] = []

if PLATFORM == 'win32':
    # On windows platform(known as win32)
    # - install mingw
    # - add it to system path(/bin folder in mingw path) !important
    import distutils.cygwinccompiler as _CYGWIN

    _CYGWIN.get_msvcr = lambda: []

    extraLinkArgs += ['-static', "-Wl,-Bstatic", "-lpthread"]
    extraCompileArgs += ['-lkernel32']

_COLORED = Extension('_colored',
                     sources=['colored.cpp'],
                     extra_compile_args=extraCompileArgs,
                     extra_link_args=extraLinkArgs,
                     language="c++")

AUTHOR = 'Arman Ahmadi'
AUTHOR_EMAIL = 'armanagha6@gmail.com'
setup(name='colorcon',
      version='0.0.1',
      description='Colored your text',
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      long_description='Not defined!',
      packages=['colorcon'],
      package_data={'colorcon': ['*']})
