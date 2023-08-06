# -*- coding: utf-8 -*-
import argparse
import logging

from gstomd.convert import GsuiteToMd


def main():

    logger = logging.getLogger("gstomd")

    logger.info("Start")
    folder_id = ""
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true"
    )
    my_parser.add_argument(
        "--debug",
        help="increase output verbosity to debug",
        action="store_true",
    )
    my_parser.add_argument(
        "--config",
        action="store",
        type=str,
        help="Configuration file for PyDrive",
        default="",
    )
    my_parser.add_argument(
        "--folder_id",
        action="store",
        type=str,
        required=True,
        help="Id of the folder to be converted",
    )

    my_parser.add_argument(
        "--dest",
        action="store",
        help="destination root folder",
        default="gstomd_extract",
    )
    args = my_parser.parse_args()

    dest_folder_name = args.dest
    folder_id = args.folder_id
    args = my_parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    gstomd = GsuiteToMd(
        dest_folder=dest_folder_name, pydrive_settings=args.config
    )
    logger.debug("gsuiteTomd  Created")

    gstomd.Folder(
        folder_id=folder_id,
    )


if __name__ == "__main__":
    # execute only if run as a script
    main()
