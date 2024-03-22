#!/usr/bin/env python3

"""
This script is an utility that expects a Construct 3 exported game ZIP file.
It will fix the cache problems that may occur when the game is served from a web server.
"""

import re

from argparse import ArgumentParser
from pathlib import Path
from random import choices
from string import ascii_letters, digits
from sys import argv
from typing import Generator
from zipfile import ZipFile

from construct_cache_fixer import logging


_logger = logging.getLogger()
_logger.setLevel(logging.INFO)

ASSETS_PATTERNS = [
    "*.css",
    "*.js",
    "*.json",
    "*.png",
    "*.ttf",
    "*.wasm",
    "*.webm"
]


def generate_random_string(length: int = 8) -> str:
    """
    Generates a random string of the specified length.

    :param length: The length of the random string to generate.
    :type length: int

    :return: The generated random string.
    :rtype: str
    """

    return "".join(choices(ascii_letters + digits, k=length))


def rename_asset(asset: Path) -> Path:
    """
    Renames the asset with a random suffix.

    :param asset: The asset to rename.
    :type asset: Path

    :return: The renamed asset.
    :rtype: Path
    """

    suffix = generate_random_string()
    new_asset = asset.with_stem(f"{asset.stem}_{suffix}")

    return new_asset


def extract_zip(archive_path: Path) -> Path:
    """
    Extracts the ZIP file to a directory.

    :param archive_path: The path to the ZIP file of the exported game.
    :type archive_path: Path

    :return: The path to the directory where the ZIP file was extracted.
    :rtype: Path
    """

    extract_path: Path = archive_path.parent / archive_path.stem
    if extract_path.exists():
        _logger.warning("The directory '%s' already exists. Skipping the extraction.", extract_path)

        return extract_path

    _logger.debug("Extracting the ZIP file '%s' to the directory: '%s'", archive_path, extract_path)

    with ZipFile(archive_path, "r") as archive:
        archive.extractall(extract_path)

    _logger.info("The ZIP file '%s' was extracted to the directory '%s'.", archive_path, extract_path)

    return extract_path


def identify_assets(extract_path: Path) -> Generator[Path, None, None]:
    """
    Identifies the assets of the game matching the defined patterns.
    
    :param extract_path: The path to the directory where the ZIP file was extracted.
    :type extract_path: Path

    :return: The list of assets of the game.
    :rtype: Generator[Path, None, None]
    """

    _logger.debug("Identifying the assets of the game in the directory: '%s'", extract_path)

    for pattern in ASSETS_PATTERNS:
        _logger.debug("Searching for assets matching the pattern: '%s'", pattern)

        for asset in extract_path.rglob(pattern):
            _logger.debug("Found an asset matching the pattern: '%s'", asset)

            yield asset

    _logger.info("The assets of the game were identified successfully.")


def search_for_asset_uses(folder_path: Path, asset: Path) -> Generator[Path, None, None]:
    """
    Searches for the uses of the asset in the source code.

    :param folder_path: The path to the directory where to search for the uses of the asset.
    :type folder_path: Path
    :param asset: The asset to search for its uses.
    :type asset: Path

    :return: The list of source files where the asset is used.
    :rtype: Generator[Path, None, None]
    """

    source_files = [
        *folder_path.rglob("*.html"),
        *folder_path.rglob("*.js"),
        *folder_path.rglob("*.json")
    ]

    _logger.debug("Looking for the uses of the asset: '%s'", asset)

    found: bool = False
    for source_file in source_files:
        asset_name = asset.stem if asset.suffix == '.webm' else asset.name
        asset_regex = re.compile(f"\\W{re.escape(asset_name)}\\W")

        _logger.debug("Looking for the uses of the assets in the source file: '%s'", source_file)

        with open(source_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if asset_regex.search(line):
                    _logger.debug("Found a use of the asset '%s' in the source file: '%s'", asset, source_file)
    
                    found = True

                    yield source_file
                    break

    if not found:
        raise FileNotFoundError(f"The asset '{asset}' was not found in the source code.")


def replace_asset_uses(source_file: Path, old_asset: Path, new_asset: Path) -> None:
    """
    Replaces the uses of the old asset with the new asset in the source file.

    :param source_file: The source file where to replace the uses of the asset.
    :type source_file: Path
    :param old_asset: The old asset to replace.
    :type old_asset: Path
    :param new_asset: The new asset to replace with.
    :type new_asset: Path

    :return: None
    """

    _logger.debug("Replacing the uses of the asset '%s' with the new asset '%s' in the source file '%s'", old_asset, new_asset, source_file)

    with open(source_file, 'r', encoding='utf-8') as file:
        content = file.read()

    old_asset_name = old_asset.stem if old_asset.suffix == '.webm' else old_asset.name
    new_asset_name = new_asset.stem if new_asset.suffix == '.webm' else new_asset.name

    content = content.replace(old_asset_name, new_asset_name)

    with open(source_file, 'w', encoding='utf-8') as file:
        file.write(content)

    _logger.info("The uses of the asset '%s' were replaced with the new asset '%s' in the source file '%s'", old_asset, new_asset, source_file)


def main() -> None:
    """
    The entry point of the script.

    :return: None
    """

    parser = ArgumentParser(description="An utility to fix the cache problems for Construct 3 exported games.")
    parser.add_argument("archive_path", help="The path to the ZIP file of the exported game.")

    args = parser.parse_args(argv[1:])

    archive_path = Path(args.archive_path)

    _logger.debug("The script was started with the archive path: '%s'", archive_path)

    if not archive_path.exists():
        raise FileNotFoundError(f"The specified file '{archive_path}' does not exist.")

    extract_path = extract_zip(archive_path)
    assets = identify_assets(extract_path)

    for asset in assets:
        _logger.debug("Looking for the uses of the asset: '%s'", asset)

        asset_uses = search_for_asset_uses(extract_path, asset)
        new_asset = rename_asset(asset)

        for asset_use in asset_uses:
            replace_asset_uses(asset_use, asset, new_asset)

        _logger.info("Renaming the asset '%s' to the new asset: '%s'", asset, new_asset.name)
        asset.rename(new_asset)

    _logger.info("The script finished its execution successfully.")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        _logger.warning("The execution was interrupted gracefully by the user.")
