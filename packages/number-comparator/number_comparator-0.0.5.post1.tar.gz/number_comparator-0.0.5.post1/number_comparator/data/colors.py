"Tool for Colorama output."

__all__ = ["Fore"]

try:
    "Import the Colorama version for colored output, then start the ANSI read."
    from colorama import init, Fore
    init(autoreset=True)
except ImportError:
    "Replace the ANSI tool to a non-colored string."
    class ForeSubstitute:
        RED = ""
        YELLOW = ""
    Fore = ForeSubstitute()
