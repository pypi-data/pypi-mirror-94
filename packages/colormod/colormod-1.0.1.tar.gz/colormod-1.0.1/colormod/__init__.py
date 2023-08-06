import colorama

def red(s: str) -> str:
    return colorama.Fore.LIGHTRED_EX + s + colorama.Fore.RESET

def blue(s: str) -> str:
    return colorama.Fore.LIGHTBLUE_EX + s + colorama.Fore.RESET

def cyan(s: str) -> str:
    return colorama.Fore.LIGHTCYAN_EX + s + colorama.Fore.RESET

def green(s: str) -> str:
    return colorama.Fore.GREEN + s + colorama.Fore.RESET

def yellow(s: str) -> str:
    return colorama.Fore.LIGHTYELLOW_EX + s + colorama.Fore.RESET

def magenta(s: str) -> str:
    return colorama.Fore.LIGHTMAGENTA_EX + s + colorama.Fore.RESET

def black(s: str) -> str:
    return colorama.Fore.LIGHTBLACK_EX + s + colorama.Fore.RESET

def white(s: str) -> str:
    return colorama.Fore.LIGHTWHITE_EX + s + colorama.Fore.RESET