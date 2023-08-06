# ------------------------------------------------------------------------------
#  Copyleft 2015-2021  PacMiam
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# ------------------------------------------------------------------------------

# Filesystem
from pathlib import Path
from shutil import rmtree

# GEM
from geode_gem.engine.api import GEM
from geode_gem.engine.utils import copy, get_data
from geode_gem.engine.lib.configuration import Configuration

from geode_gem.ui.data import Icons, Columns, Folders, Metadata
from geode_gem.ui.utils import magic_from_file

# Logging
from logging import getLogger

# System
from argparse import ArgumentParser
from os import environ

# Translation
from gettext import textdomain, bindtextdomain
from gettext import gettext as _


# ------------------------------------------------------------------------------
#   Launcher
# ------------------------------------------------------------------------------

def copy_file(path, new_path):
    """

    Parameters
    ----------
    path : pathlib.Path
        Original file path to copy
    new_path : pathlib.Path
        Destination path

    Returns
    -------
    bool
        True is copy is successful, False, otherwise
    """

    if path.exists() and not new_path.exists():
        copy(path, new_path)
        return True

    return False


def make_directory(path, mode=0o755, make_parents=True):
    """ Generate a directory

    Parameters
    ----------
    path : pathlib.Path
        Directory path
    mode : octal integer, optional
        Directory access permissions
    make_parents : bool, optional
        Ensure to create all the directories from path if missing

    Returns
    -------
    bool
        True is creation is successful, False, otherwise
    """

    if not path.exists():
        path.mkdir(mode=mode, parents=make_parents)
        return True

    return False


def init_localization(egg_name):
    """ Initialize application localization

    Parameters
    ----------
    egg_name : str
        Python egg name
    """

    bindtextdomain(egg_name, localedir=str(get_data("data", "i18n")))
    textdomain(egg_name)


def init_environment():
    """ Initialize main environment

    Returns
    -------
    geode_gem.engine.lib.configuration.Configuration
        Metadata configuration file instance for testing purpose
    """

    # Initialize metadata
    metadata = Configuration(get_data("data", "config", "metadata.conf"))

    # Retrieve metadata informations
    if metadata.has_section("metadata"):
        for key, value in metadata.items("metadata"):
            setattr(Metadata, key.upper(), value)

    # Retrieve icons informations
    if metadata.has_section("icons"):
        for key, value in metadata.items("icons"):
            setattr(Icons, key.upper(), value)
            setattr(Icons.Symbolic, key.upper(), f"{value}-symbolic")

    if metadata.has_section("icon-sizes"):
        for key, value in metadata.items("icon-sizes"):
            setattr(Icons.Size, key.upper(), value.split())

    # Retrieve columns informations
    if metadata.has_section("misc"):
        setattr(Columns, "ORDER",
                metadata.get("misc", "columns_order", fallback=str()))

    if metadata.has_section("list"):
        for key, value in metadata.items("list"):
            setattr(Columns.List, key.upper(), int(value))

    if metadata.has_section("grid"):
        for key, value in metadata.items("grid"):
            setattr(Columns.Grid, key.upper(), int(value))

    return metadata


def init_configuration(gem):
    """ Initialize user configuration

    Parameters
    ----------
    gem : gem.engine.api.GEM
        GEM API instance
    """

    move_collection = False

    # Configuration
    for filename in ("gem.conf", "consoles.conf", "emulators.conf"):
        path = get_data("data", "config", filename)
        new_path = gem.get_config(filename)

        if copy_file(path, new_path):
            gem.logger.debug(f"Copy {path} to {new_path}")

    # Local
    for folder in ("logs", "notes"):
        if make_directory(gem.get_local(folder)):
            gem.logger.debug(f"Generate {folder} directory")

    # Cache
    for name in ("consoles", "emulators", "games"):
        for size in getattr(Icons.Size, name.upper(), list()):
            path = Folders.CACHE.joinpath(name, f"{size}x{size}")

            if make_directory(path):
                gem.logger.debug(f"Generate {path} directory")

    # Icons
    icons_path = gem.get_local("icons")

    if not icons_path.exists():
        if make_directory(icons_path):
            gem.logger.debug(f"Generate {icons_path} directory")

        move_collection = True

    # Remove older icons collections folders (GEM < 1.0)
    else:
        for folder in ("consoles", "emulators"):
            path = icons_path.joinpath(folder)

            if not path.exists():
                continue

            if path.is_dir():
                rmtree(path)

            elif path.is_symlink():
                path.unlink()

            move_collection = True

    # Copy default icons
    if move_collection:
        gem.logger.debug("Generate consoles icons folder")

        for filename in get_data("data", "icons").glob("*.png"):

            if not filename.is_file():
                continue

            # Check the file mime-type to avoid non-image file
            mime = magic_from_file(filename, mime=True)
            if mime.startswith("image/"):
                new_path = icons_path.joinpath(filename.name)

                if copy_file(filename, new_path):
                    gem.logger.debug(f"Copy {filename} to {new_path}")


def main():
    """ Main launcher
    """

    # Initialize localization
    init_localization("geode_gem")

    # Initialize environment
    init_environment()

    # ----------------------------------------
    #   Generate arguments
    # ----------------------------------------

    parser = ArgumentParser(
        epilog=Metadata.COPYLEFT,
        description=f"{Metadata.NAME} - {Metadata.VERSION}",
        conflict_handler="resolve")

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{Metadata.NAME} {Metadata.VERSION} "
                f"({Metadata.CODE_NAME}) - {Metadata.LICENSE}",
        help="show the current version")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="launch gem with debug flag")

    parser_api = parser.add_argument_group("api arguments")
    parser_api.add_argument(
        "--cache",
        action="store",
        metavar="FOLDER",
        default=Folders.Default.CACHE,
        help=f"set cache folder (default: {Folders.Default.CACHE})")
    parser_api.add_argument(
        "--config",
        action="store",
        metavar="FOLDER",
        default=Folders.Default.CONFIG,
        help=f"set configuration folder (default: {Folders.Default.CONFIG})")
    parser_api.add_argument(
        "--local",
        action="store",
        metavar="FOLDER",
        default=Folders.Default.LOCAL,
        help=f"set data folder (default: {Folders.Default.LOCAL})")

    parser_maintenance = parser.add_argument_group("maintenance arguments")
    parser_maintenance.add_argument(
        "--clean-cache",
        action="store_true",
        help="clean icons cache directory")

    arguments = parser.parse_args()

    # ----------------------------------------
    #   Cache directory
    # ----------------------------------------

    setattr(Folders, "CACHE",
            Path(arguments.cache, "gem").expanduser().resolve())
    make_directory(Folders.CACHE)

    if Folders.CACHE.exists() and arguments.clean_cache:

        if Folders.CACHE.is_dir():
            rmtree(Folders.CACHE)

        if not Folders.CACHE.exists():
            Folders.CACHE.mkdir(mode=0o755, parents=True)

    # ----------------------------------------
    #   Launch interface
    # ----------------------------------------

    process_status = False

    try:
        gem = GEM(arguments.config, arguments.local, arguments.debug)

        # Set cache directory
        cache_path = Folders.Default.CACHE.joinpath(gem.Instance)

        # Check display settings
        if "DISPLAY" in environ and environ.get("DISPLAY"):

            if not gem.is_locked():
                # Initialize main configuration files
                init_configuration(gem)

                getLogger(gem.Instance).info(f"Start GEM with PID {gem.pid}")

                # Start splash
                from geode_gem.ui.splash import Splash
                Splash(gem)

                # Start interface
                from geode_gem.ui.interface import MainWindow
                MainWindow(gem, cache_path)

                # Remove lock
                gem.free_lock()

            else:
                getLogger(gem.Instance).critical(
                    f"GEM is already running with PID {gem.pid}")

                from geode_gem.ui.splash import Message
                message = Message(
                    _("An instance already exists"),
                    _("GEM is already running with PID %s") % gem.pid)
                message.run()

        else:
            getLogger(gem.Instance).critical(
                "Cannot launch GEM without display")

    except ImportError:
        getLogger("gem").exception("An error occur durint modules importation")
        process_status = True

    except KeyboardInterrupt:
        getLogger("gem").warning("Terminate by keyboard interrupt")
        process_status = True

    except Exception:
        getLogger("gem").exception("An error occur during execution")
        process_status = True

    # Remove lock when an error occurs
    if process_status:
        gem.free_lock()

    return process_status


if __name__ == "__main__":
    main()
