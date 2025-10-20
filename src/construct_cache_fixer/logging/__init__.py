import logging
import os

from inspect import FrameInfo, getmodule, stack
from types import ModuleType
from typing import Optional

from .colored_logging import ColoredLogger


NOTSET: int = logging.NOTSET
DEBUG: int = logging.DEBUG
INFO: int = logging.INFO
WARNING: int = logging.WARNING
ERROR: int = logging.ERROR
CRITICAL: int = logging.CRITICAL


__default_level__: int | str = os.environ.get("LOGGING_LEVEL", INFO)


def getLogger(name: Optional[str] = None, level: Optional[int | str] = None) -> ColoredLogger:
    if not name:
        frame: FrameInfo = stack()[1]
        module: ModuleType = getmodule(frame[0])
        name = module.__name__

    if not level:
        level = __default_level__

    return ColoredLogger(name=name, level=level)


def setLevel(level: Optional[int | str] = None) -> None:
    global __default_level__

    if not level:
        level = INFO

    __default_level__ = level
