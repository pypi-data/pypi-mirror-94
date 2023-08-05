import builtins

from xonsh.completers import completer
from xonsh.completers.tools import RichCompletion
from .utils import run


def fish_proc_completer(prefix: str, line: str, begidx, endidx, ctx):
    """Populate completions using fish shell and remove bash-completer"""
    output = run()
    return {
        RichCompletion(
            str(row[0]),
            description=str(row[0]),
            style="bg:ansiyellow fg:ansiblack",
        )
        for row in c.fetchall()
    }


completer.add_one_completer(
    "fish",
    fish_proc_completer,
    # "start"
)
completer.remove_completer("bash")
