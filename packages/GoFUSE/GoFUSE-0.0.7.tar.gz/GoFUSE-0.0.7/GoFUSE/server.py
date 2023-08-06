#!/usr/bin/env python3

import errno
import logging
import os
import sys
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

from fuse import FUSE, FuseOSError, Operations

SERVER_URL = os.environ.get('SERVER_URL', '0.0.0.0:5000')
LOGLEVEL = getattr(logging, os.environ.get('LOGLEVEL', 'ERROR'))

logging.basicConfig(
    format='%(asctime)s [%(process)s] %(levelname)s %(pathname)s:%(lineno)s: %(message)s',  # NOQA E501
    # filename=basename_executable + '.log',
    # level=logging.INFO,
    level=LOGLEVEL,
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def wrap_exeptions(func):

    def wrapper(*args, **kwargs):
        logger.debug(f"Calling:{repr(func)} args:{repr(args)} kwargs:{repr(kwargs)})")
        data = None
        exception = None
        try:
            data = func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            exception = repr(e)
        logger.debug(f"data:{repr(data)}")
        logger.debug(f"exception:{repr(exception)}")
        return {
            'data': data,
            'exception': exception,
        }

    return wrapper

class Passthrough(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    @wrap_exeptions
    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    @wrap_exeptions
    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    @wrap_exeptions
    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    @wrap_exeptions
    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        data = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                    'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        return data

    @wrap_exeptions
    def getxattr(self, path, attribute, follow_symlinks=True):
        full_path = self._full_path(path)
        data = os.getxattr(full_path, attribute, follow_symlinks=follow_symlinks)
        return data

    @wrap_exeptions
    def readdir(self, path, fh):
        full_path = self._full_path(path)
        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        return dirents

    @wrap_exeptions
    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    @wrap_exeptions
    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    @wrap_exeptions
    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    @wrap_exeptions
    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    @wrap_exeptions
    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    @wrap_exeptions
    def unlink(self, path):
        return os.unlink(self._full_path(path))

    @wrap_exeptions
    def symlink(self, name, target):
        return os.symlink(name, self._full_path(target))

    @wrap_exeptions
    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    @wrap_exeptions
    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    @wrap_exeptions
    def utimens(self, path, times):
        times = tuple(times)
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    @wrap_exeptions
    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    @wrap_exeptions
    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    @wrap_exeptions
    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        data = os.read(fh, length)
        return data

    @wrap_exeptions
    def write(self, path, buf, offset, fh):
        buf = buf.data
        os.lseek(fh, offset, os.SEEK_SET)
        data = os.write(fh, buf)
        return data

    @wrap_exeptions
    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    @wrap_exeptions
    def flush(self, path, fh):
        return os.fsync(fh)

    @wrap_exeptions
    def release(self, path, fh):
        return os.close(fh)

    @wrap_exeptions
    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)


def main():

    # Get configuration
    server_name, server_port = SERVER_URL.split(':')
    server_port = int(server_port)
    root_dir = sys.argv[1]

    # Create server
    logger.info(f"Starting server on {server_name}:{server_port}")
    with SimpleXMLRPCServer(
        (server_name, server_port),
        requestHandler=SimpleXMLRPCRequestHandler,
        logRequests=False,
        allow_none=True,
    ) as server:

        server.register_introspection_functions()
        server.register_instance(Passthrough(root_dir))

        # Run the server's main loop
        logger.debug(f"Serving directory '{root_dir}'")
        server.serve_forever()

if __name__ == '__main__':
    main()
    