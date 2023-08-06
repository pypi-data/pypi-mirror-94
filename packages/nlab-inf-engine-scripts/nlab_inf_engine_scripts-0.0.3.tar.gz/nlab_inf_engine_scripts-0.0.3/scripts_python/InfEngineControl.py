#!/usr/bin/python3

import argparse
import logging

from colorama import Fore, Style
from scripts_python.InfEngineServer import InfEngineServer


def main():
    def success():
        print(f"    {Fore.GREEN}[SUCCESS]{Style.RESET_ALL}\n")

    def failure():
        print(f"    {Fore.RED}[FAILED]{Style.RESET_ALL}\n")

    parser = argparse.ArgumentParser(description="Manipulate InfEngine server.")
    parser.add_argument(
        "--root-path",
        action="store",
        nargs=1,
        default=None,
        metavar="ROOT_PATH",
        help=f"Default path: {InfEngineServer().root_path}",
    )

    group = parser.add_argument_group("Logging").add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        action="store_true",
        help=f"Enable INFO level logging.",
    )
    group.add_argument(
        "-vv",
        action="store_true",
        help=f"Enable DEBUG level logging.",
    )

    group = parser.add_argument_group("InfServer").add_mutually_exclusive_group()
    group.add_argument("--start", action="store_true", help=f"Start InfServer.")
    group.add_argument("--stop", action="store_true", help=f"Stop InfServer.")
    group.add_argument("--restart", action="store_true", help=f"Restart InfServer.")
    group.add_argument("--respawn", action="store_true", help=f"Respawn InfServer.")
    group.add_argument("--status", action="store_true", help=f"Get InfServer status.")
    group.add_argument(
        "--version", action="store_true", help=f"Print versions and exit."
    )
    group.add_argument(
        "--dl-update", action="store",
        nargs=1,
        default=None,
        metavar="DL_DATA_PATH",
        help=f"Update DL data (binary or sources)."
    )
    group.add_argument(
        "--dl-delete", action="store",
        nargs=1,
        default=None,
        metavar="DL_DATABASE_PATH",
        help=f"Delete given DL data."
    )
    group.add_argument(
        "--dl-delete-all", action="store_true", help=f"Delete all DL data."
    )

    args = parser.parse_args()

    root_path = args.root_path[0] if args.root_path else None

    if args.v:
        logging_level = logging.INFO
    elif args.vv:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.ERROR

    print("\n    InfEngine Manager\n")

    server = InfEngineServer(root_path=root_path, logging_level=logging_level)

    try:
        if args.start:
            print(" * Starting InfServer", end="")
            server.start()
            success()
        elif args.stop:
            print(" * Stopping InfServer", end="")
            server.stop()
            success()
        elif args.restart:
            print(" * Restarting InfServer", end="")
            server.restart()
            success()
        elif args.respawn:
            print(" * Respawning InfServer", end="")
            server.respawn()
            success()
        elif args.status:
            print(" * Getting InfServer status", end="")
            status = server.status()
            success()
            print(f"InfServer status: {status}\n")
        elif args.version:
            print(f"InfEngineServer: {InfEngineServer.VERSION}\n")
        elif args.dl_update:
            print(" * Update data", end="")
            server.update_data(dldata=args.dl_update)
            success()
        elif args.dl_delete:
            print(" * Delete data", end="")
            server.delete_dl(database_name=args.dl_delete)
            success()
        elif args.dl_delete_all:
            print(" * Delete all data", end="")
            server.delete_dl_all()
            success()
        else:
            parser.print_help()
            print()
    except Exception as e:
        failure()
        print(f"\n{e}\n")


if __name__ == "__main__":
    main()
