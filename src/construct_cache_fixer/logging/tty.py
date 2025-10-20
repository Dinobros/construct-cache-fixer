import os
import platform

from typing import List, Optional


__OS__: str = platform.system()


class TextFormat:
    DEFAULT: str = '0'
    BOLD: str = '1'
    DIM: str = '2'
    UNDERLINE: str = '3'
    BLINK: str = '5'
    REVERSE: str = '7'
    HIDDEN: str = '8'


class TextColor:
    DEFAULT: str = '39'
    BLACK: str = '30'
    DARK_RED: str = '31'
    DARK_GREEN: str = '32'
    DARK_YELLOW: str = '33'
    BLUE: str = '34'
    DARK_MAGENTA: str = '35'
    DARK_CYAN: str = '36'
    LIGHT_GRAY: str = '37'
    GRAY: str = '90'
    RED: str = '91'
    GREEN: str = '92'
    YELLOW: str = '93'
    LIGHT_BLUE: str = '94'
    MAGENTA: str = '95'
    CYAN: str = '96'
    WHITE: str = '97'


class BackgroundColor:
    DEFAULT: str = '49'
    BLACK: str = '40'
    DARK_RED: str = '41'
    DARK_GREEN: str = '42'
    DARK_YELLOW: str = '43'
    BLUE: str = '44'
    DARK_MAGENTA: str = '45'
    DARK_CYAN: str = '46'
    LIGHT_GRAY: str = '47'
    GRAY: str = '100'
    RED: str = '101'
    GREEN: str = '102'
    YELLOW: str = '103'
    LIGHT_BLUE: str = '104'
    MAGENTA: str = '105'
    CYAN: str = '106'
    WHITE: str = '107'


def clear() -> None:
    os.system('cls' if __OS__ == 'Windows' else 'clear')


def pretty(text: str, text_color: Optional[str] = None,
                      text_format: Optional[str] = None,
                      background_color: Optional[str] = None) -> str:

    args: List[str] = []

    if text_color:
        #
        # TODO: Check if 'text_color' is valid!
        #
        args.append(text_color)

    if text_format:
        #
        # TODO: Check if 'text_format' is valid!
        #
        args.append(text_format)

    if background_color:
        #
        # TODO: Check if 'background_color' is valid!
        #
        args.append(background_color)

    attrs = ";".join(args)

    return f"\033[{attrs}m{text}\033[0m"


if __OS__ == 'Windows':
    #
    # TODO: Make the colors look great even on Windows platform!
    #
    def plain(text: str, **_) -> str:
        return text

    pretty = plain
