# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/logging.ipynb.

# %% auto 0
__all__ = [
    "console",
    "print",
    "reset_logger_width",
    "logger",
    "Debug",
    "Info",
    "Warn",
    "Excep",
    "get_console",
    "reset_logger",
    "enter_exit",
]

# %% ../nbs/logging.ipynb 3
from rich.console import Console
from rich.theme import Theme
from loguru import logger
from datetime import datetime
from fastcore.basics import patch_to, ifnone
from rich.logging import RichHandler
from pathlib import Path

# from torch_snippets.ipython import is_in_notebook

from functools import wraps
import time

# %% ../nbs/logging.ipynb 4
def get_console(width=None):
    return Console(
        width=width,
        theme=Theme(
            {
                "repr.number": "bold cyan",
                "repr.string": "bold green",
                "logging.level.info": "dim yellow",
                "logging.level.warning": "dim red",
                "logging.level.exception": "bold red",
            }
        ),
    )


console = get_console()
print = console.print

# %% ../nbs/logging.ipynb 7
@patch_to(RichHandler)
def render(
    self,
    *,
    record,
    traceback,
    message_renderable: "ConsoleRenderable",
) -> "ConsoleRenderable":
    """patched the renderer to print function name as well"""
    path = Path(record.pathname).name
    level = self.get_level_text(record)
    time_format = None if self.formatter is None else self.formatter.datefmt
    log_time = datetime.fromtimestamp(record.created)

    log_renderable = self._log_render(
        self.console,
        [message_renderable] if not traceback else [message_renderable, traceback],
        log_time=log_time,
        time_format=time_format,
        level=level,
        path=path,
        line_no=f"{record.funcName}:{record.lineno}",
        link_path=record.pathname if self.enable_link_path else None,
    )
    return log_renderable


def reset_logger(level="INFO", width=172, silent=True):
    if level is not None:
        [logger.remove() for _ in range(100)]
        logger.configure(
            handlers=[
                {
                    "sink": RichHandler(
                        rich_tracebacks=True,
                        console=console,
                        tracebacks_show_locals=False,
                    ),
                    "format": "<level>{message}</level>",
                    "backtrace": True,
                    "level": level,
                }
            ],
        )
    if width is not None:
        for handler_id in logger._core.handlers:
            try:
                handler = logger._core.handlers[handler_id]
                handler._sink._handler.console = get_console(width=width)
            except:
                ...
    if not silent:
        logger.info(f"reset logger's console width to {width} and level to {level}!")


reset_logger_width = lambda width: reset_logger(width=width)

reset_logger(width=100, silent=True)
reset_logger(width=100, silent=True)

logger = logger

Debug = lambda x, depth=0: logger.opt(depth=depth + 1).log("DEBUG", x)
Info = lambda x, depth=0: logger.opt(depth=depth + 1).log("INFO", x)
Warn = lambda x, depth=0: logger.opt(depth=depth + 1).log("WARNING", x)
Excep = lambda x, depth=0: logger.opt(depth=depth + 1).log("ERROR", x)

# %% ../nbs/logging.ipynb 10
def enter_exit(func):
    """
    Logs the time taken to execute a function along with entry & exit time stamps
    """
    logger_ = logger.opt(depth=1)

    @wraps(func)
    def function_timer(*args, **kwargs):
        tic = time.time()
        logger_.log("DEBUG", f"Entered function `{func.__name__}`")
        o = func(*args, **kwargs)
        toc = time.time()
        logger_.log(
            "DEBUG", f"Exiting function `{func.__name__}` after {toc-tic:.3f} seconds"
        )
        return o

    return function_timer
