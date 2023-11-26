import logging
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from click import ClickException

from ftp2webdav.config import build_configuration
from ftp2webdav.server import FTP2WebDAV

app = typer.Typer()

DEFAULT_CONFIG_FILE_PATHS = (
    Path("~/.ftp2webdav.conf").expanduser(),
    Path("/etc/ftp2webdav.conf"),
)


@app.command()
def run(
        *,
        config_file: Annotated[Optional[Path], typer.Option(
            "--config", "-c",
            help="Path to config file.",
        )] = None,
        verbose: Annotated[bool, typer.Option(
            "--verbose", "-v",
            help="Verbose output.",
        )] = False,
):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)-15s %(levelname)-8s %(message)s')

    # Find config file
    if config_file is None:
        for file in DEFAULT_CONFIG_FILE_PATHS:
            if file.exists():
                config_file = file
                break

    if config_file is None or not config_file.exists():
        raise ClickException("No configuration file found.")

    try:
        with config_file.open() as fh:
            config = build_configuration(yaml.safe_load(fh))
    except yaml.YAMLError as err:
        raise ClickException(f"Invalid YAML in configuration file: {config}") from err

    ftp = FTP2WebDAV(
        webdav_config=config['webdav'],
        target_dir=Path(config['target_dir']),
        ftp_host=config['ftp']['host'],
        ftp_port=config['ftp']['port'],
    )
    ftp.start()
