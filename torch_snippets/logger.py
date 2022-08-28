# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/logging.ipynb (unless otherwise specified).

__all__ = ['get_console', 'console', 'print', 'render', 'logger', 'Debug', 'Info', 'Warn', 'Excep',
           'reset_logger_width']

# Cell
from rich.console import Console
from rich.theme import Theme


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

# Cell
from loguru import logger
from datetime import datetime
from fastcore.basics import patch_to
from rich.logging import RichHandler
from pathlib import Path


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


logger.configure(handlers=[{
    "sink":RichHandler(
        rich_tracebacks=True,
        console=console,
        tracebacks_show_locals=False
    ),
    "format":'<level>{message}</level>',
    "backtrace": True
}])

logger = logger

Debug = lambda x, depth=0: logger.opt(depth=depth + 1).log("DEBUG", x)
Info = lambda x, depth=0: logger.opt(depth=depth + 1).log("INFO", x)
Warn = lambda x, depth=0: logger.opt(depth=depth + 1).log("WARNING", x)
Excep = lambda x, depth=0: logger.opt(depth=depth + 1).log("ERROR", x)

# Cell
from .ipython import is_in_notebook

def reset_logger_width(logger, width):
    for handler_id in logger._core.handlers:
        try:
            handler = logger._core.handlers[handler_id]
            handler._sink._handler.console = get_console(width=width)
            logger.info(f"reset logger's console width to {width}!")
        except:
            ...

# Excep("TESTING {1,2,3}")
# if is_in_notebook():
#     reset_logger_width(logger, 115)
# Excep("TESTING {1,2,3}")