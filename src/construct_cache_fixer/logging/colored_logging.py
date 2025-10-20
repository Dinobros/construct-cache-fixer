import logging

from logging import Formatter, Logger, LogRecord, StreamHandler
from typing import Dict, Optional

from . import tty
from .tty import TextColor


__FORMAT__: str = '[%(asctime)s] %(levelname)s (%(name)s on %(processName)s[%(threadName)s]): %(message)s'
__DATE_FORMAT__: str = '%d/%m/%Y %H:%M:%S'
__LEVEL_COLORS__: Dict[int, str] = {
    50: TextColor.RED,
    40: TextColor.DARK_RED,
    30: TextColor.DARK_YELLOW,
    20: TextColor.DARK_GREEN,
    10: TextColor.LIGHT_BLUE,
    0: TextColor.GRAY
}


class ColoredFormatter(Formatter):
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        if not fmt:
            fmt = __FORMAT__

        if not datefmt:
            datefmt = __DATE_FORMAT__

        Formatter.__init__(self, fmt, datefmt)

    def format(self, record: LogRecord) -> str:
        level_color: str = __LEVEL_COLORS__[record.levelno]
        record.levelname = tty.pretty(record.levelname, text_color=level_color)

        return Formatter.format(self, record)


class ColoredLogger(Logger):
    @staticmethod
    def GetHandler() -> StreamHandler:
        # pylint: disable=invalid-name

        handler = StreamHandler()
        formatter = ColoredFormatter()

        handler.setFormatter(formatter)

        return handler

    def __init__(self, name: str, level: Optional[int | str] = None):
        if not level:
            level: int = logging.INFO

        super().__init__(name, level)

        handler: StreamHandler = ColoredLogger.GetHandler()

        self.addHandler(handler)
        self.propagate = False
