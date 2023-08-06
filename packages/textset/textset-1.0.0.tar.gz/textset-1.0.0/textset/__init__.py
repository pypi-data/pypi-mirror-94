###It's textset module.
from sys import version as _version
_python_version = _version[0:3] # get python version
_string = True
if not float(_python_version)> 3.5:
    _string = False
    
class text:
    global _string
    def coloring(value, color):
        if _string:
            return f'\033[0m \033[9{str(color)}m {str(value)}'
        else: # python 3.5 version can't use f-string
            return '\033[0m \033[9{}m {}'.format(str(color), str(value))
    def underline(value):
        if _string:
            return f'\033[0m \033[4m{str(value)}'
        else:
            return '\033[0m \033[4m{}'.format(str(value))
    def highlight(value):
        if _string:
            return f'\033[0m \033[1m {str(value)}'
        else:
            return '\033[0m \033[1m {}'.format(str(value))

if __name__ == '__main__':
    print('Your python version is..', _python_version)
    print(text.highlight('hello, world'))
    print(text.underline('hello, world'))
    print(text.coloring('hello, world', 4))