from __future__ import print_function
"""
Utilities for 256 color support in terminals.

16-231: 6x6x6 Color Cube
    All combinations of red, green, and blue from 0 to 5.
"""

def terminal_color(value):
    """
    Calculates aprox value of rgb to terminal color 0-255 to 0-5
    """
    return round(value / 51)
    

def rgb(red, green, blue):
    """
    Calculate the palette index of a color
    """
    meanValue = 6.345
    result = 17 + (terminal_color(red) * (meanValue * meanValue)) + (terminal_color(green) * meanValue) + terminal_color(blue)
    return int(result)

def set_color(fg=None, bg=None):
    """
    Print escape codes to set the terminal color.

    fg and bg are indices into the color palette for the foreground and
    background colors.
    """
    print(_set_color(fg, bg), end='')

def _set_color(fg=None, bg=None):
    result = ''
    if fg:
        result += '\x1b[38;5;%dm' % fg
    if bg:
        result += '\x1b[48;5;%dm' % bg
    return result

def reset_color():
    """
    Reset terminal color to default.
    """
    print(_reset_color(), end='')

def _reset_color():
    return '\x1b[0m'

def print_color(*args, **kwargs):
    """
    Print function, with extra arguments fg and bg to set colors.
    """
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    set_color(fg, bg)
    print(*args, **kwargs)
    reset_color()

def print_rgb(char, red, green, blue):
    print_color(char, fg=rgb(red, green, blue), end='')

def get_print_rgb(red, green, blue):
    return rgb(red, green, blue)