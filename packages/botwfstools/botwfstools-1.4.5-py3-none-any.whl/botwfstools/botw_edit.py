#!/usr/bin/env python3
# Copyright 2018 leoetlino <leo@leolam.fr>
# Licensed under MIT

import argparse
import colorama # type: ignore
from colorama import Fore, Style # type: ignore
import os
import subprocess
import signal
import sys
import tempfile
import typing

def _spawn(args):
    if os.name == 'nt':
        return subprocess.Popen(args, stdout=subprocess.DEVNULL, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    return subprocess.Popen(args, stdout=subprocess.DEVNULL, preexec_fn=os.setpgrp)

def main(content_dir: typing.List[str], content_view: str, work_dir: str, patched_view: typing.Optional[str], target: str, patch_dir: typing.Optional[str]) -> None:
    this_dir = os.path.dirname(os.path.abspath(__file__))

    if not patched_view and not patch_dir:
        sys.stderr.write('error: please pass --patched-view and/or --patch-dir, otherwise this tool cannot do much\n')
        sys.exit(1)

    TMP_PREFIX = 'botw-edit-tmp-'
    with tempfile.TemporaryDirectory(prefix=TMP_PREFIX) as temp_merged_dir, \
         tempfile.TemporaryDirectory(prefix=TMP_PREFIX) as temp_patch_dir:

        # WinFsp limitation: mountpoints must not exist.
        if os.name == 'nt':
            os.rmdir(temp_merged_dir)

        if not patch_dir:
            patch_dir = temp_patch_dir

        # Mount overlayfs: content_dirs... -> merged_dir
        overlayfs_p1 = _spawn([sys.executable, os.path.join(this_dir, 'botw_overlayfs.py'),
                               *content_dir, temp_merged_dir])
        print(temp_merged_dir)
        # Mount contentfs: content_dirs... work_dir -> content_view (work: work_dir)
        # Note that we do not use the merged view to reduce overhead
        contentfs_p = _spawn([sys.executable, os.path.join(this_dir, 'botw_contentfs.py'),
                              *content_dir, content_view, '-w', work_dir])
        overlayfs_p2 = None
        if patched_view:
            # Mount overlayfs: content_dirs... patch_dir -> patched_view (work: patch_dir)
            overlayfs_p2 = _spawn([sys.executable, os.path.join(this_dir, 'botw_overlayfs.py'),
                                   *content_dir, patched_view, '-w', patch_dir])

        def signal_handler(sig, frame):
            sys.stderr.write('exiting...\n')
            for process in [overlayfs_p2, contentfs_p, overlayfs_p1]:
                if not process:
                    continue
                if os.name == 'nt':
                    process.terminate()
                else:
                    process.send_signal(signal.SIGINT)
                process.wait()

            if os.name == 'nt':
                os.mkdir(temp_merged_dir)
            sys.exit(0)

        def run_patcher():
            sys.stderr.write('\n')
            sys.stderr.write(f'{Style.DIM}--------------- Running patcher ---------------{Style.RESET_ALL}\n')
            try:
                subprocess.run([sys.executable, os.path.join(this_dir, 'botw_patcher.py'), temp_merged_dir,
                               work_dir, patch_dir, '--force', '--target', target], check=True)
            except subprocess.CalledProcessError:
                sys.stderr.write(f'{Style.BRIGHT}{Fore.RED}Patcher exited with non-zero code{Style.RESET_ALL}\n')
                signal_handler(None, None)
            sys.stderr.write(f'{Style.BRIGHT}{Fore.GREEN}done.{Style.RESET_ALL}\n')
            print_information()

        signal.signal(signal.SIGINT, signal_handler)
        if os.name != 'nt':
            signal.signal(signal.SIGUSR1, lambda sig, frame: run_patcher())
        sys.stderr.write('Ready.\n')
        def print_information():
            sys.stderr.write('\n')
            sys.stderr.write(f'Content view: {Fore.BLUE}{content_view}{Style.RESET_ALL}\n')
            sys.stderr.write(f'Work directory: {Fore.BLUE}{work_dir}{Style.RESET_ALL}\n')
            if TMP_PREFIX not in patch_dir:
                sys.stderr.write(f'Patch dir: {Fore.BLUE}{patch_dir}{Style.RESET_ALL}\n')
            if patched_view:
                sys.stderr.write(f'Patched view: {Fore.BLUE}{patched_view}{Style.RESET_ALL}\n')
            sys.stderr.write('\n')
            sys.stderr.write(f'{Style.BRIGHT}{Fore.WHITE}To update game files, type \'patch\'{Style.RESET_ALL}\n')
        print_information()

        while True:
            cmd = input()
            if cmd != 'patch':
                continue
            run_patcher()

def cli_main() -> None:
    colorama.init()
    parser = argparse.ArgumentParser(description='Wrapper for overlayfs and contentfs to allow editing and testing game files easily.')
    parser.add_argument('content_dir', nargs='+', help='Paths to content directories. Directories take precedence over the ones on their left.')
    parser.add_argument('--content-view', help='Path to the directory on which the extracted view should be mounted', required=True)
    parser.add_argument('--work-dir', help='Path to the directory where modified and new files will be stored', required=True)
    parser.add_argument('--patch-dir', help='Path to the patch dir', required=False)
    parser.add_argument('--patched-view', help='Path to the patched content view', required=False)
    parser.add_argument('--target', choices=['wiiu', 'switch'], help='Target platform', required=True)
    args = parser.parse_args()

    main(args.content_dir, args.content_view, args.work_dir, args.patched_view, args.target, args.patch_dir)

if __name__ == '__main__':
    cli_main()
