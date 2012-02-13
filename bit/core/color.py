import sys

# I hate how I have to do all this setup just for windows, but oh well :/
if sys.platform == 'win32':
    from ctypes import windll, Structure, byref
    from ctypes import c_ushort as ushort, c_short as short

    class Coord(Structure):
        _fields_ = [('X', short), ('Y', short)]

    class SmallRect(Structure):
        _fields_ = [(x, short) for x in ('Left', 'Top', 'Right', 'Bottom')]

    class ConsoleScreenBufferInfo(Structure):
        _fields_ = [
            ('size', Coord),
            ('cursor_position', Coord),
            ('attributes', ushort),
            ('window', SmallRect),
            ('maximum_window_size', Coord)
        ]

    __handle = windll.kernel32.GetStdHandle(-11)

    def __get_console():
        csbi = ConsoleScreenBufferInfo()
        windll.kernel32.GetConsoleScreenBufferInfo(__handle, byref(csbi))
        return csbi.attributes

    set_console = windll.kernel32.SetConsoleTextAttribute
    default_colors = __get_console()

    __win32_colors = [
        0x0, # black
        0x4, # red
        0x2, # green
        0x6, # yellow
        0x1, # blue
        0x5, # magenta
        0x3, # cyan
        0x7  # white
    ]

def __private_print(color, text, output):
    if sys.platform == 'win32':
        set_console(__handle, __win32_colors[color] | 0x8 & 0xFF0F)
    else: text = '\33[1;3{}m{}\33[0m'.format(color, text)
    print(text, end='', file=output)
    if sys.platform == 'win32': set_console(__handle, default_colors)

def __stdout(color, text): __private_print(color, text, sys.stdout)
def __stderr(color, text): __private_print(color, text, sys.stderr)

class __color(object):
    def __init__(self):
        self.__dict__ = { name:idx for idx, name in \
            enumerate(('black', 'red', 'green', 'yellow',
                       'blue', 'magenta', 'cyan', 'white'))
        }

colors = __color()

def command(msg): __stdout(colors.magenta, '{}\n'.format(msg))
def warning(msg): __stdout(colors.yellow, '{}\n'.format(msg))
def success(msg): __stdout(colors.green, '{}\n'.format(msg))
def error(msg): __stderr(colors.red, '{}\n'.format(msg))
def info(msg): __stdout(colors.cyan, '{}\n'.format(msg))

__all__ = ['command', 'warning', 'success', 'error', 'info']
