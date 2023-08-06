"""
High level API for _colored written in c++
"""

from typing import (
    Collection,
    List,
    Tuple,
    Dict,
)

import _colored


def __asObjects(_T: type):
    """Convert class attributes to hashmap

    usage:
      for calling class methods with string(hashmap)
    example:
      class klass:
        member = 2

        __asObjects(klass) -> {'member': 2}
    :param type _T: class
    :return: hashmap of class members names and value
    :rtype: dict[str, any]
    """
    return {colorName.lower(): colorValue
            for colorName, colorValue in _T.__dict__.items()
            if not colorName.startswith('_')}


class COLORS:
    # @formatter:off
    Black    = (0, 0, 0)
    White    = (255, 255, 255)
    Red      = (255, 51, 51)
    Yellow   = (255, 255, 51)
    Green    = (102, 255, 102)
    Blue     = (102, 102, 255)
    Purple   = (178, 102, 255)
    Orange   = (255, 153, 51)

    Default  = Black
    # @formatter:on


_ALL_COLORS: Dict[str, Tuple[int, int, int]] = __asObjects(COLORS)


class MODES:
    Bold = 1
    Light = 2
    Italic = 4
    Underline = 8
    SlowBlink = 16
    RapidBlink = 32
    Reverse = 64


_ALL_MODES: Dict[str, int] = __asObjects(MODES)

# Exceptions
INVALID_COLOR_LITERAL = 'all color(RGB) must be type of int and smaller than 128 and bigger than(-1)'
COLOR_NOT_FOUND = "can't find color in store!"
INVALID_MODE = "mode isn't correct"
MODE_NOT_FOUND = "can't find mode in store!"


def RGB2hex(rgbColor) -> str:
    """Convert RGB color to hex

    :param  List[int, int, int] or Tuple[int, int, int] rgbColor: contain tree value(red, green, blue)
    :return: rgb color converted to hex(start with '#')
    :rtype: str
    """
    return '#' + hex(
        (rgbColor[0] << 16)  # red
        + (rgbColor[1] << 8)  # green
        + rgbColor[2])[2:]  # blue


def hex2RGB(hexColor) -> Tuple[int, int, int]:
    """Covert hex to RGB

    :param str hexColor: hex color that can start with '#' or not!
    :return: tuple of converted color from hex, Contain tree color(red, green, blue)
    :rtype tuple
    """
    hexColor = hexColor.replace(' ', '')
    intColor = int(hexColor[1
                            if hexColor[0] == '#'  # if color start with #(mean its hex), remove it
                            else 0:], 16)
    return (intColor >> 16 & 255,  # red
            intColor >> 8 & 255,  # green
            intColor & 255)  # blue


def _check_color(color) -> Tuple[int, int, int] or None:
    """Check color is valid or not!

    :param list[int, int, int] or tuple[int, int, int] or str color: Can be RGB or hex
    :return: tuple with tree color(red, green, blue)
    :rtype: Tuple[int, int, int] or None
    :raises AttributeError: if color isn't in default colors
    :raises Exception: if color isn't valid
    """
    if color is None:
        return None
    if isinstance(color, str):
        if color[0] == '#':  # for hex colors
            return hex2RGB(color)
        color = color.lower()
        if color not in _ALL_COLORS:  # pick color from store
            reset_all()
            raise AttributeError(COLOR_NOT_FOUND)
        return _ALL_COLORS[color]
    if isinstance(color, list):
        if not all(map(lambda c: (isinstance(c, int)
                                  and 0 <= c <= 255), color)):
            reset_all()
            raise TypeError(INVALID_COLOR_LITERAL)
        return tuple(color)
    reset_all()
    raise Exception(COLOR_NOT_FOUND)


def _check_modes(*modes) -> List[int]:
    """Check modes is valid or not!

    :param int or str modes: Can be RGB or hex
    :return: tuple with modes in int
    :rtype: Tuple[int]
    :raises AttributeError: if mode isn't in default modes
    :raises Exception: if mode isn't valid
    """
    if not modes:
        return []
    mode = modes[0]
    out = []
    if isinstance(mode, str):
        if mode not in _ALL_MODES:
            reset_all()
            raise AttributeError(MODE_NOT_FOUND)
        out = _check_modes(_ALL_MODES[mode])
    elif isinstance(mode, int):
        i = 1
        while mode:
            c = mode % 2 * i
            if c:
                out += [i]
            i += 1
            mode //= 2
    elif not isinstance(mode, list):
        reset_all()
        raise Exception(INVALID_MODE)
    return out + _check_modes(*modes[1:])


def output(*texts: str,
           sep: str = ' ') -> None:
    """Print text in stdout from c!
    output will be flush automatically

    :param str texts: texts will be printed!
    :param str sep: separator for texts!
      separator is '-'
      output of ('hello', 'im', 'test') is 'hello-im-test'
    """
    _colored.output(sep.join(map(str, texts)))


def set_background(bgColor) -> None:
    """Set color of background!

    :param List[int, int, int] or Tuple[int, int, int] or str bgColor: Can be in rgb or hex
    """
    bgColor = _check_color(bgColor)
    if bgColor:
        _colored.begin_background()
        _colored.set_color(list(bgColor))


def set_foreground(fgColor) -> None:
    """Set color of foreground!

    :param List[int, int, int] or Tuple[int, int, int] or str fgColor: Can be in rgb or hex
    """
    fgColor = _check_color(fgColor)
    if fgColor:
        _colored.begin_foreground()
        _colored.set_color(list(fgColor))


def set_mode(*modes) -> None:
    """Set mode for console

    :param Collection modes: Given modes in str or int
    """
    for m in _check_modes(*modes):
        _colored.set_mode(m)


def reset_all() -> None:
    """Reset all ansi formatting,
    Convert to normal console
    """
    _colored.reset()


def colored(text,
            bgColor=None,
            fgColor=None,
            modes=(),
            end='\n') -> None:
    """Make console colored with given colors(background and foreground)
    Then print text into output, (!Console will reset after)

    default colors are:
      red, blue, white, black, purple, green, yellow, orange

    default modes are:
      bold, light, italic, underline, slowblink, rapidblink, reverse

      !Some of modes may not work in all consoles

    default end is '\\n'

    examples:
      output of colored('hello of test', 'red', 'blue', ('bold',)) will be text with red background and blue foreground and bold effect
    :param any text: text will be colored
    :param List[int, int, int] or Tuple[int, int, int] or str bgColor: Color of background(default is None)
    :param List[int, int, int] or Tuple[int, int, int] or str fgColor: Color of foreground(default is None)
    :param Collection[int] or Collection[str] modes: Modes for formatted output!
    :param str end: Print at end of colored text(default is '\n')
    """
    set_background(bgColor)
    set_foreground(fgColor)
    set_mode(*modes)
    output(str(text))
    reset_all()
    output(end)
