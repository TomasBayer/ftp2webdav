import logging
import os

import easywebdav
# TODO: Replace this dirty workaround for amnong/easywebdav#26
import easywebdav.client
from ftprelay import AuthenticationFailedError, FTPRelay

from ftp2webdav.config import build_configuration

easywebdav.basestring = str
easywebdav.client.basestring = str

logger = logging.getLogger(__name__)

basestring = (str, bytes)


class FTP2WebDAV(FTPRelay):

    def __init__(self, raw_config):
        self.config = build_configuration(raw_config)
        self.target_dir = self.config['target_dir']
        self.webdav_config = self.config['webdav']

        super().__init__((self.config['ftp']['host'], self.config['ftp']['port']), self._file_processor_creator)

    def _file_processor_creator(self, username, password):

        webdav_client = easywebdav.connect(username=username, password=password, **self.webdav_config)

        # Check authentication
        try:
            webdav_client.exists(self.target_dir)
        except easywebdav.OperationFailed as ex:
            if ex.actual_code == 401:
                raise AuthenticationFailedError()
            else:
                raise ex

        return lambda file: self._send_file(file, webdav_client)

    def _send_file(self, file, webdav_client):
        # Create necessary directories
        webdav_client.mkdirs(self.target_dir)

        # Upload file
        print(os.path.join(self.target_dir, os.path.basename(file)))
        webdav_client.upload(file, os.path.join(self.target_dir, os.path.basename(file)))

        logger.info('File was uploaded successfully.')
