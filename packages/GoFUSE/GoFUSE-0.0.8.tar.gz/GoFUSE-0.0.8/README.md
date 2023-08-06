# GoFUSE

## Description

GoFUSE is a pyfuse / xmlrpc based distributed filesystem. It can be used to quickly share files across an network in testing or development environments.


## Installation

GoFUSE depends on FUSE, the 'Filesystem in Userspace' interface. On MacOS you can install the necessary kernel extension with Homebrew using `brew install --cask osxfuse`. On Linux you could run `sudo apt install libfuse`. The installation of GoFUSE itself is pretty straight forward.

```
pip3 install GoFUSE
```


## Usage

```
python3 -m GoFUSE.server <directory>
python3 -m GoFUSE.client <mountpoint>
```

### Example

To run the GOFUSE server process on localhost (port 5001) you can run this:
```
SERVER_URL=127.0.0.1:5001 python3 -m GoFUSE.server .
```

Afterh the server has been started you can mount the directory the server is publishing with the client like this:
```
SERVER_URL=127.0.0.1:5001 python3 -m GoFUSE.client /mnt/data/
```


## Options

Some GoFUSE internals can be changed using enviromnent variables:

  * SERVER_URL: Define IP/FQDN and port

    - Default: "0.0.0.0:5000"
    - Examples: "127.0.0.1:5001", "192.168.0.1:8080"

  * LOGLEVEL: Change verbosity of logging

    - Default: "ERROR"
    - Examples: "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"

  * PROTOCOL: Change access protocol

    - Default: "http://"
    - Example: "https://"
    - Note: This is only available for the client. If you want to change the protocol the server is using you must use a proxy (that is not included here). This feature is experimental and untested.


## Known issues

In docker environments you might have to run containers in *privileged* mode in order to be able to inject the FUSE extension that is needed.

This filesystem implementation is not intended to be used in production environments - sendig all data via xmlrpc has a rather big overhead and will most likely lead to problems when larger files are transmitted.
