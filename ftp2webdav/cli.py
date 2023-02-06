import argparse
import logging
import sys
from pathlib import Path

import yaml

from ftp2webdav.config import build_configuration
from ftp2webdav.server import FTP2WebDAV


def build_argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-file', '-c', type=Path, help="config file")
    parser.add_argument('--verbose', '-v', action='store_true', help="verbose mode")

    return parser


def run():
    parser = build_argparser()
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)-15s %(levelname)-8s %(message)s')

    # Find config file
    config_file = None
    if args.config_file:
        config_file = args.config_file.expanduser()
    else:
        for file in (Path("~/.ftp2webdav.conf").expanduser(), Path("/etc/ftp2webdav.conf")):
            if file.exists():
                config_file = file
                break

    if config_file is None:
        sys.exit("No configuration file found.")

    try:
        with config_file.open() as fh:
            config = build_configuration(yaml.safe_load(fh))
    except yaml.YAMLError:
        sys.exit(f"Invalid YAML in configuration file: {config}")

    ftp = FTP2WebDAV(
        webdav_config=config['webdav'],
        target_dir=Path(config['target_dir']),
        ftp_host=config['ftp']['host'],
        ftp_port=config['ftp']['port'],
    )
    ftp.start()
