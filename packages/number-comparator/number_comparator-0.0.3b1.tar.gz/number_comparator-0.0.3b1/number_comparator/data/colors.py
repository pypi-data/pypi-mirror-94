"Tool for Colorama output."

__all__ = ["Fore"]

try:
    from colorama import init, Fore
    init(autoreset=True)
except ImportError:
    class ForeSubstitute:
        RED = ""
        YELLOW = ""
    Fore = ForeSubstitute()
