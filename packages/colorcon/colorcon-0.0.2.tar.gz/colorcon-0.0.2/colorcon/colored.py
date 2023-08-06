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
    Black   = (0, 0, 0)
    White   = (255, 255, 255)
    Red     = (255, 51, 51)
    Yellow  = (255, 255, 51)
    Green   = (102, 255, 102)
    Blue    = (102, 102, 255)
    Purple  = (178, 102, 255)
    Orange  = (255, 153, 51)

    Default = Black
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


def RGB2hex(rgb_color) -> str:
    """Convert RGB color to hex

    :param  List[int, int, int] or Tuple[int, int, int] rgb_color: contain tree value(red, green, blue)
    :return: rgb color converted to hex(start with '#')
    :rtype: str
    """
    return '#' + hex(
        (rgb_color[0] << 16)  # red
        + (rgb_color[1] << 8)  # green
        + rgb_color[2])[2:]  # blue


def hex2RGB(hex_color) -> Tuple[int, int, int]:
    """Covert hex to RGB

    :param str hex_color: hex color that can start with '#' or not!
    :return: tuple of converted color from hex, Contain tree color(red, green, blue)
    :rtype tuple
    """
    hex_color = hex_color.replace(' ', '')
    int_color = int(hex_color[1
                              if hex_color[0] == '#'  # if color start with #(mean its hex), remove it
                              else 0:], 16)
    return (int_color >> 16 & 255,  # red
            int_color >> 8 & 255,  # green
            int_color & 255)  # blue


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


def set_background(bg_color) -> None:
    """Set color of background!

    :param List[int, int, int] or Tuple[int, int, int] or str bg_color: Can be in rgb or hex
    """
    bg_color = _check_color(bg_color)
    if bg_color:
        _colored.begin_background()
        _colored.set_color(list(bg_color))


def set_foreground(fg_color) -> None:
    """Set color of foreground!

    :param List[int, int, int] or Tuple[int, int, int] or str fg_color: Can be in rgb or hex
    """
    fg_color = _check_color(fg_color)
    if fg_color:
        _colored.begin_foreground()
        _colored.set_color(list(fg_color))


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
            bg_color=None,
            fg_color=None,
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
    :param List[int, int, int] or Tuple[int, int, int] or str bg_color: Color of background(default is None)
    :param List[int, int, int] or Tuple[int, int, int] or str fg_color: Color of foreground(default is None)
    :param Collection[int] or Collection[str] modes: Modes for formatted output!
    :param str end: Print at end of colored text(default is '\n')
    """
    set_background(bg_color)
    set_foreground(fg_color)
    set_mode(*modes)
    output(str(text))
    reset_all()
    output(end)
