# ftp2webdav

`ftp2webdav` is an FTP server that forwards all uploaded files to a WebDAV server.
It was developed with the specific goal of retrofitting a [Nextcloud](https://nextcloud.com/) interface into older
devices or software that exclusively support FTP upload for file transfer.

**Caution:** `ftp2webdav` has not undergone security testing. Avoid exposing it to untrusted networks or the public
internet without implementing proper security measures.

## Quick Navigation

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Features

* FTP user authentication seamlessly validates against the WebDAV server
* Lightweight and fast (uses `pyftpdlib` underneath)
* Easy YAML configuration

## Installation

Requires Python version 3.9 or higher and pip.

```bash
pip install ftp2webdav
```

## Configuration

To configure `ftp2webdav`, a configuration file is required. By default, the program looks for it
in `~/.ftp2webdav.conf` or `/etc/ftp2webdav`. Create a sample configuration file with:

```bash
ftp2webdav --create-example-config
```

### Example Configuration File

```yaml
---
ftp:
  host: 127.0.0.1
  port: 21

webdav:
  host: webdav.host
  port: 443
  protocol: https
  path: uri/path/to/webdav/endpoint
  verify_ssl: True
  cert: /path/to/cert

target_dir: path/to/target/dir/
```

- FTP server configuration (`ftp`):
    - `host`: Specifies the FTP server's IP address or hostname.
    - `port`: Specifies the FTP server's port.
- WebDAV Server configuration (`webdav`):
    - `host`: Specifies the hostname or IP address of the WebDAV server.
    - `port`: Specifies the port of the WebDAV server.
    - `protocol`: Specifies the protocol used for WebDAV communication.
    - `path`: Defines the URI path to the WebDAV endpoint.
    - `verify_ssl`: Boolean indicating whether to verify SSL certificates.
    - `cert`: Path to the (local) SSL certificate used for secure communication.
- Target Directory Configuration (`target_dir`):
    - Specifies the path to the target directory on the WebDAV server where uploaded files should be stored.

## Usage

Run the server:

```bash
ftp2webdav
```

### File Upload

Log into the server using valid user credentials of the WebDAV sever, and then upload a file. The uploaded file will be
automatically stored in the directory specified in the config file.

### Caveats

- There are no subfolders on the FTP server, nor does it allow the creation of any. Thus, all files must be directly
  uploaded to the root directory.
- Using interactive FTP browsers to access the server may result in errors, as they are restricted from reading the
  contents of the root directory.

## License

`ftp2webdav` is distributed under the terms of the MIT License.
