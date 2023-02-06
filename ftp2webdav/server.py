import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import easywebdav
from ftprelay import AuthenticationFailedError, Authenticator, FileProcessor, FTPRelay

# TODO: Replace this dirty workaround for https://github.com/amnong/easywebdav/issues/26
easywebdav.basestring = str
easywebdav.client.basestring = str

logger = logging.getLogger(__name__)


@dataclass
class WebDAVFileUploader(FileProcessor):
    webdav_client: easywebdav.Client
    target_dir: Path

    def process_file(self, file: Path) -> None:
        # Create necessary directories
        self.webdav_client.mkdirs(str(self.target_dir))

        # Upload file
        self.webdav_client.upload(str(file), str(self.target_dir / file.name))

        logger.info('File was uploaded successfully.')


@dataclass
class WebDAVAuthenticator(Authenticator):
    webdav_config: dict[str, Any]
    target_dir: Path

    def authenticate(self, username: str, password: str) -> FileProcessor:
        webdav_client = easywebdav.connect(username=username, password=password, **self.webdav_config)

        # Check authentication
        try:
            webdav_client.exists(self.target_dir)
        except easywebdav.OperationFailed as err:
            if err.actual_code == 401:
                raise AuthenticationFailedError() from err
            else:
                raise err

        return WebDAVFileUploader(webdav_client, self.target_dir)


@dataclass
class FTP2WebDAV:
    webdav_config: dict[str, Any]
    target_dir: Path
    ftp_host: str
    ftp_port: int

    relay: FTPRelay = field(init=False, default=None)

    def __post_init__(self):
        self.relay = FTPRelay(
            authenticator=WebDAVAuthenticator(self.webdav_config, self.target_dir),
            host=self.ftp_host,
            port=self.ftp_port,
        )

    def start(self):
        self.relay.start()

    def stop(self):
        self.relay.stop()
