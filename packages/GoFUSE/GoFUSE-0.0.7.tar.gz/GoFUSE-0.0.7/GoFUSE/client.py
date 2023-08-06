#!/usr/bin/env python

import errno
import logging
import os
import sys
import xmlrpc.client

from fuse import FUSE, FuseOSError, Operations

SERVER_URL = os.environ.get('SERVER_URL', 'localhost:5000')
LOGLEVEL = getattr(logging, os.environ.get('LOGLEVEL', 'ERROR'))
PROTOCOL = os.environ.get('PROTOCOL', 'http://')

logging.basicConfig(
    format='%(asctime)s [%(process)s] %(levelname)s %(pathname)s:%(lineno)s: %(message)s',  # NOQA E501
    # filename=basename_executable + '.log',
    # level=logging.INFO,
    level=LOGLEVEL,
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def unwrap_exceptions_generator(func):
    def wrapper_generator(self, *args, **kwargs):
        data = self._call(func, *args, **kwargs)
        for i in data['data']:
            yield i
    return wrapper_generator

def unwrap_exceptions(func):
    def wrapper(self, *args, **kwargs):
        data = self._call(func, *args, **kwargs)
        return data['data']
    return wrapper

class Passthrough(Operations):

    def __init__(self, server_name, server_port):
        logger.info(f"Opening {server_name}:{server_port} for a GoFUSE mount!")
        self.server = xmlrpc.client.ServerProxy(
            f'{PROTOCOL}{server_name}:{server_port}/',
            allow_none=True,
        )
        logger.debug(self.server.system.listMethods())

    # Helper
    def _unpack(self, data):
        if isinstance(data['data'], xmlrpc.client.Binary):
            data['data'] = data['data'].data
        return data
    
    def _call(self, func, *args, **kwargs):
        logger.debug(f"Calling:{repr(func)} args:{repr(args)} kwargs:{repr(kwargs)})")
        callable = getattr(self.server, func.__name__)
        data = callable(*args, **kwargs)
        data = self._unpack(data)
        if data['exception'] is not None:
            exec(f"raise {data['exception']}")
        logger.debug(f"Data type is {type(data['data'])}")
        return data

    # Filesystem methods
    # ==================

    @unwrap_exceptions
    def access(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def chmod(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def chown(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def getattr(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def getxattr(self, *args, **kwargs):
        pass

    # Generator
    @unwrap_exceptions_generator
    def readdir(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def readlink(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def mknod(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def rmdir(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def mkdir(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def statfs(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def unlink(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def symlink(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def rename(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def link(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def utimens(self, *args, **kwargs):
        pass

    # File methods
    # ============

    @unwrap_exceptions
    def open(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def create(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def read(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def write(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def truncate(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def flush(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def release(self, *args, **kwargs):
        pass

    @unwrap_exceptions
    def fsync(self, *args, **kwargs):
        pass


def main():

    # Get configuration
    server_name, server_port = SERVER_URL.split(':')
    server_port = int(server_port)
    mountpoint = sys.argv[1]

    # Create client
    logger.info(f"Starting client fo {server_name}:{server_port}")
    logger.debug(f"Mounting '{mountpoint}'")
    FUSE(Passthrough(server_name, server_port), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main()
