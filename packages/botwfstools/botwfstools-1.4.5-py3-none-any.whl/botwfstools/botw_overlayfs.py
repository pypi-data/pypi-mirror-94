#!/usr/bin/env python3
# Copyright 2018 leoetlino <leo@leolam.fr>
# Licensed under MIT

import argparse
import errno
import os
from pathlib import Path
import shutil
import sys
import typing

from fuse import FUSE, FuseOSError, Operations # type: ignore

BINARY_MODE = os.O_BINARY if os.name == 'nt' else 0

class BotWMergedContent(Operations):
    """Similar to overlayfs. More assumptions but simpler and should work on Windows."""

    def __init__(self, content_dir: typing.List[str], work_dir: typing.Optional[str]) -> None:
        self.content_dir = content_dir
        self.work_dir = work_dir
        self.path_cache: typing.Dict[str, str] = dict()
        self.stat_cache: typing.Dict[str, dict] = dict()
        self.readdir_cache: typing.Dict[str, set] = dict()

    def _real_path(self, partial: str) -> str:
        """Get a host FS path based on the content dir list and the work directory.
        File precedence: work_dir, content_dir[n-1], ..., content_dir[0]
        """
        if not self.work_dir and partial in self.path_cache:
            return self.path_cache[partial]
        if self.work_dir:
            path = self.work_dir + partial
            if os.path.exists(path):
                return path
        for directory in reversed(self.content_dir):
            path = directory + partial
            if os.path.exists(path):
                self.path_cache[partial] = path
                return path
        raise FuseOSError(errno.ENOENT)

    def access(self, path, mode):
        if os.name == 'nt':
            return
        real_path = self._real_path(path)
        if not os.access(real_path, mode):
            raise FuseOSError(errno.EACCES)

    def getattr(self, path, fh=None):
        if not self.work_dir and path in self.stat_cache:
            return self.stat_cache[path]
        real_path = self._real_path(path)
        st = os.lstat(real_path)
        d = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
        if os.name != 'nt':
            d['st_blocks'] = st.st_blocks
        if not self.work_dir:
            self.stat_cache[path] = d
        return d

    def readdir(self, path, fh) -> typing.Iterator[str]:
        entries = set(['.', '..'])

        if self.work_dir:
            real_path = self.work_dir + path
            if os.path.isdir(real_path):
                entries.update(os.listdir(real_path))

        for directory in reversed(self.content_dir):
            real_path = directory + path
            if os.path.isdir(real_path):
                l = os.listdir(real_path)
                entries.update(l)

        for r in entries:
            yield r

    def rmdir(self, path):
        if not self.work_dir or not os.path.exists(self.work_dir + path):
            raise FuseOSError(errno.EROFS)
        return os.rmdir(self.work_dir + path)

    def mkdir(self, path, mode):
        if not self.work_dir:
            raise FuseOSError(errno.EROFS)
        # Check if the parent path exists -- an error will be raised if it doesn't
        self._real_path(str(Path(path).parent))
        return os.makedirs(self.work_dir + path, mode)

    def statfs(self, path):
        real_path = self._real_path(path)
        if os.name == 'nt':
            usage = shutil.disk_usage(str(real_path))
            return {
                # Just return everything in bytes.
                'f_frsize': 1,
                'f_blocks': usage.total,
                'f_bfree': usage.free,
            }

        stv = os.statvfs(real_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        if not self.work_dir or not os.path.exists(self.work_dir + path):
            raise FuseOSError(errno.EROFS)
        return os.unlink(self.work_dir + path)

    def rename(self, old, new):
        if not self.work_dir or not os.path.exists(self.work_dir + old):
            raise FuseOSError(errno.EROFS)
        return os.rename(self.work_dir + old, self.work_dir + new)

    def utimens(self, path, times=None):
        return os.utime(self._real_path(path), times)

    def open(self, path, flags):
        real_path = self._real_path(path)
        if (flags & os.O_WRONLY or flags & os.O_RDWR):
            if not self.work_dir:
                raise FuseOSError(errno.EROFS)
            if not os.path.exists(self.work_dir + path):
                os.makedirs(self.work_dir + str(Path(path).parent), exist_ok=True)
                shutil.copyfile(real_path, self.work_dir + path)

        return os.open(self._real_path(path), flags | BINARY_MODE)

    def create(self, path, mode, fi=None):
        if not self.work_dir:
            raise FuseOSError(errno.EROFS)
        parent_dir = str(Path(path).parent)
        # Check whether the parent path exists.
        self._real_path(parent_dir)
        os.makedirs(self.work_dir + parent_dir, exist_ok=True)
        return os.open(self.work_dir + path, os.O_RDWR | os.O_CREAT | BINARY_MODE, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        if not self.work_dir:
            raise FuseOSError(errno.EROFS)
        with open(self.work_dir + path, 'r+b') as f:
            f.truncate(length)

    def flush(self, path, fh):
        pass

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)

def _exit_if_not_dir(path: str):
    if not os.path.isdir(path):
        sys.stderr.write('error: %s is not a directory\n' % path)
        sys.exit(1)

def main(content_dir: typing.List[str], target_dir: str, work_dir: typing.Optional[str]) -> None:
    for directory in content_dir:
        _exit_if_not_dir(directory)
    if work_dir:
        _exit_if_not_dir(work_dir)

    for directory in content_dir:
        print('content: %s' % directory)
    print('target: %s' % target_dir)
    if work_dir:
        print('work: %s' % work_dir)
    else:
        print('work: (none, read-only)')
    if os.name != 'nt':
        FUSE(BotWMergedContent(content_dir, work_dir), target_dir, nothreads=True, foreground=True)
    else:
        FUSE(BotWMergedContent(content_dir, work_dir), target_dir, nothreads=True, foreground=True,
             uid=65792, gid=65792, umask=0)

def cli_main() -> None:
    parser = argparse.ArgumentParser(description='Presents a merged content view and transparently redirects modifications to another directory.')
    parser.add_argument('content_dir', nargs='+', help='Paths to content directories. Directories take precedence over the ones on their left.')
    parser.add_argument('target_mount_dir', help='Path to the directory on which the merged view should be mounted')
    parser.add_argument('-w', '--workdir', help='Path to the directory where modified/new files will be stored')

    args = parser.parse_args()
    main(content_dir=args.content_dir, target_dir=args.target_mount_dir, work_dir=args.workdir)

if __name__ == '__main__':
    cli_main()
