#!/usr/bin/env python3
# Copyright 2018 leoetlino <leo@leolam.fr>
# Licensed under MIT

import argparse
from collections import defaultdict
import colorama # type: ignore
from colorama import Fore, Style # type: ignore
import io
import os
from pathlib import Path
import rstb, rstb.util
import sarc
import shutil
import oead
import sys
import typing
import re

ARCHIVE_EXTS = {'sarc', 'pack', 'bactorpack', 'bmodelsh', 'beventpack', 'stera', 'stats',
                'ssarc', 'spack', 'sbactorpack', 'sbmodelsh', 'sbeventpack', 'sstera', 'sstats',
                'blarc', 'sblarc', 'genvb', 'sgenvb'}
AOC_PREFIX = 'Aoc/0010/'
AOC_PREFIX_LIST = (
    'Terrain/A/AocField',
    'UI/StaffRollDLC/',
    'Map/MainField/',
    'Map/MainFieldDungeon/',
    'Map/AocField/',
    'Physics/StaticCompound/AocField/',
    'Physics/StaticCompound/MainFieldDungeon/',
    'Movie/Demo6',
    'Game/AocField/',
    'NavMesh/AocField/',
    'NavMesh/MainFieldDungeon/',
    'Physics/TeraMeshRigidBody/AocField/',
    'System/AocVersion.txt',
    'Pack/RemainsWind.pack',
    'Pack/RemainsElectric.pack',
    'Pack/RemainsWater.pack',
    'Pack/RemainsFire.pack',
    'Pack/FinalTrial.pack')
AOC_VOICE_PATTERN = re.compile('^Voice/.*/Stream_Demo6.*/.*\.bfstm$')

def _is_archive_filename(path: Path) -> bool:
    return path.suffix[1:] in ARCHIVE_EXTS

def _exists(path: Path) -> bool:
    if os.name != 'nt':
        return path.exists()

    # Work around a Windows limitation with FUSE-like mountpoints.
    try:
        return path.exists()
    except OSError:
        # Windows returns 'Incorrect function' on a WinFsp mountpoint.
        return True

def _is_dir(path: Path) -> bool:
    if os.name != 'nt':
        return path.is_dir()

    # Work around a Windows limitation with FUSE-like mountpoints.
    try:
        return path.is_dir()
    except OSError:
        # Windows returns 'Incorrect function' on a WinFsp mountpoint.
        return True

def _compress_file(path: Path) -> None:
    data = bytes()
    with open(path, 'rb') as f:
        data = oead.yaz0.compress(f.read())

    compressed_path = path
    if not path.suffix.startswith('.s'):
        compressed_path = path.with_suffix('.s' + path.suffix[1:])

    with open(compressed_path, 'wb') as f:
        f.write(data)

    if not path.suffix.startswith('.s'):
        path.unlink()

def _get_parents_and_path(path: Path):
    for parent in reversed(path.parents):
        yield parent
    yield path

def _find_sarc(path: Path) -> typing.Optional[sarc.SARC]:
    archive: typing.Optional[sarc.SARC] = None
    archive_path: str = ''
    for i, p in enumerate(_get_parents_and_path(path)):
        if _exists(p) and _is_dir(p):
            continue

        if archive:
            path_in_archive = p.relative_to(archive_path).as_posix()
            if path_in_archive not in archive.list_files():
                continue
            archive = sarc.read_file_and_make_sarc(
                io.BytesIO(archive.get_file_data(path_in_archive).tobytes()))
            if not archive:
                return None
        else:
            try:
                with p.open('rb') as f:
                    archive = sarc.read_file_and_make_sarc(f) # type: ignore
                    archive_path = p
                    if not archive:
                        return None
            except:
                return None

    return archive

def is_gamedata_archive_file_name(file_name: str):
    return file_name == 'gamedata.ssarc' or file_name == 'savedataformat.ssarc'

def repack_archive(content_dir: Path, archive_path: Path, rel_archive_dir: Path, wiiu: bool) -> bool:
    temp_archive_dir = archive_path.with_name(archive_path.name + '.PATCHER_TEMP')
    os.rename(archive_path, temp_archive_dir)

    archive = _find_sarc(content_dir / rel_archive_dir)
    if archive:
        writer = sarc.make_writer_from_sarc(archive, lambda x: True)
    else:
        writer = sarc.SARCWriter(wiiu)
    if not writer:
        return False

    for root, dirs, files in os.walk(temp_archive_dir, topdown=False):
        for file_name in files:
            host_file_path = Path(os.path.join(root, file_name))
            path_in_archive = host_file_path.relative_to(temp_archive_dir).as_posix()
            # For some reason, Nintendo uses paths with leading slashes in these archives. Annoying.
            if is_gamedata_archive_file_name(archive_path.name):
                path_in_archive = '/' + path_in_archive
            with open(host_file_path, 'rb') as f:
                writer.add_file(path_in_archive, f.read())

    with open(archive_path, 'wb') as archive_file:
        writer.write(archive_file)

    if archive_path.suffix.startswith('.s'):
        sys.stderr.write('compressing...\n')
        _compress_file(archive_path)
    shutil.rmtree(temp_archive_dir)
    return True

_RSTB_PATH_IN_CONTENT = 'System/Resource/ResourceSizeTable.product.srsizetable'
_RSTB_BLACKLIST = {'Actor/ActorInfo.product.byml'}
_RSTB_BLACKLIST_ARCHIVE_EXT = {'.blarc', '.sblarc', '.genvb', '.sgenvb', '.bfarc', '.sbfarc'}
_RSTB_BLACKLIST_SUFFIXES = {'.pack', '.yml', '.yaml', '.aamp', '.xml'}

size_calculator = rstb.SizeCalculator()

def _should_be_listed_in_rstb(resource_path: Path, rel_path: Path) -> bool:
    if str(resource_path) in _RSTB_BLACKLIST:
        return False
    for parent in rel_path.parents:
        if is_gamedata_archive_file_name(parent.name):
            return False
        if parent.suffix in _RSTB_BLACKLIST_ARCHIVE_EXT:
            return False
    return resource_path.suffix not in _RSTB_BLACKLIST_SUFFIXES

def _fix_rstb_resource_size(path: Path, rel_path: Path, table: rstb.ResourceSizeTable, wiiu: bool, is_aoc: bool):
    resource_path = _get_resource_path_for_rstb(rel_path, is_aoc)
    if not _should_be_listed_in_rstb(Path(resource_path), rel_path=rel_path):
        sys.stderr.write(f'{Fore.WHITE}{rel_path}{Style.RESET_ALL} ({resource_path})\n')
        return
    resource_size = size_calculator.calculate_file_size(str(path), wiiu=wiiu)
    if resource_size == 0:
        sys.stderr.write(f'{Fore.WHITE}{rel_path}{Style.RESET_ALL} ({resource_path}) {Style.BRIGHT}{Fore.YELLOW}*** complex ***{Style.RESET_ALL}\n')
        table.delete_entry(resource_path)
        return

    notes = []
    prev_resource_size = 0
    if not table.is_in_table(resource_path):
        notes.append(f'{Style.BRIGHT}{Fore.RED}*** NEW ***{Style.RESET_ALL}')
    else:
        prev_resource_size = table.get_size(resource_path)

    sys.stderr.write(f'{Fore.WHITE}{rel_path}{Style.RESET_ALL} ({resource_path}) [0x%x -> 0x%x bytes] %s\n'
        % (prev_resource_size, resource_size, ' '.join(notes)))
    table.set_size(resource_path, resource_size)

def _get_resource_path_for_rstb(rel_path: Path, is_aoc: bool) -> str:
    """Get the RSTB resource path for a resource file."""
    rel_path = rel_path.with_suffix(rel_path.suffix.replace('.s', '.'))

    for parent in rel_path.parents:
        if _is_archive_filename(parent):
            return get_path(rel_path.relative_to(parent).as_posix(), is_aoc)

    # File is not in any archive, so just return the path relative to the content root.
    return get_path(rel_path.as_posix(), is_aoc)

def get_path(path: str, is_aoc: bool) -> str:
    """Add aoc prefix to resource path if necessary"""

    if path.startswith('001'):
        new_path = path[5:]
    else:
        new_path = path

    if not is_aoc:
        return path

    if new_path.startswith(AOC_PREFIX_LIST) or AOC_VOICE_PATTERN.match(new_path):
        return AOC_PREFIX + new_path

    num_match = re.search('Dungeon(\d\d\d)', new_path)
    if num_match:
        if int(num_match[1]) > 119:
            if new_path.startswith('Pack/') and new_path.endswith('.pack'):
                return AOC_PREFIX + new_path
            if new_path.startswith(('Map/CDungeon/', 'Physics/StaticCompound/', 'NavMesh/CDungeon/')):
                return AOC_PREFIX + new_path

    return path

def make_loadable_layer(content_dir: Path, patch_dir: Path, target_dir: Path, wiiu: bool, table: rstb.ResourceSizeTable, is_aoc: bool):
    """Converts an extracted content patch view into a loadable content layer.

    Directories that have an SARC extension in their name will be recursively repacked as archives.
    """

    # Copy files to the target directory so that we don't trash the original files.
    shutil.copytree(str(patch_dir), str(target_dir))

    # Build a list of files and directories that need to be patched.
    files_by_depth: typing.DefaultDict[int, typing.List[Path]] = defaultdict(list)
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            files_by_depth[full_path.count(os.path.sep)].append(Path(full_path))
        for file_name in dirs:
            full_path = os.path.join(root, file_name)
            files_by_depth[full_path.count(os.path.sep)].append(Path(full_path))

    size_calculator = rstb.SizeCalculator()

    for depth in sorted(files_by_depth.keys(), reverse=True):
        for file in files_by_depth[depth]:
            rel_path = file.relative_to(target_dir)
            # Repack any extracted archive.
            if _is_dir(file) and _is_archive_filename(file):
                sys.stderr.write(f'repacking {Fore.CYAN}%s{Style.RESET_ALL}...\n' % rel_path)
                repack_archive(content_dir=content_dir, archive_path=file, rel_archive_dir=rel_path, wiiu=wiiu)
            if not file.is_file():
                continue

            # TODO: support arbitrary file conversions (contentfs needs to be modified too),
            # for example yaml -> byml, bxml -> xml.


            # Fix the size in the RSTB *before* compression.
            _fix_rstb_resource_size(path=file, rel_path=rel_path, table=table, wiiu=wiiu, is_aoc=is_aoc)

            # TODO: automatically compress file types that are managed by the resource system
            # and that are not already in a compressed archive (excluding pack, bfevfl
            # bcamanim and barslist).

def _fail_if_not_dir(path: Path):
    if not path.is_dir():
        sys.stderr.write('error: %s is not a directory\n' % path)
        sys.exit(1)

def cli_main() -> None:
    colorama.init()

    parser = argparse.ArgumentParser(description='Converts an extracted content patch directory into a loadable content layer.')
    parser.add_argument('content_dir', type=Path, help='Path to the game content directory')
    parser.add_argument('patch_dir', type=Path, help='Path to the extracted content patch directory')
    parser.add_argument('target_dir', type=Path, help='Path to the target directory')
    parser.add_argument('-f', '--force', action='store_true', help='Clean up the target directory if it exists')
    parser.add_argument('-t', '--target', choices=['wiiu', 'switch'], help='Target platform', required=True)
    parser.add_argument('--aoc_dir', type=Path, help='Path to the game add-on-content directory')
    parser.add_argument('--aoc_patch_dir', type=Path, help='Path to the extracted add-on-content patch directory')
    parser.add_argument('--aoc_target_dir', type=Path, help='Path to the target add-on-content directory')

    args = parser.parse_args()

    # These would always fail on Windows because of WinFsp.
    if os.name != 'nt':
        _fail_if_not_dir(args.content_dir)
        _fail_if_not_dir(args.patch_dir)

    if args.target_dir.is_dir():
        shutil.rmtree(args.target_dir)

    if os.path.exists(args.target_dir) and len(os.listdir(args.target_dir)) != 0:
        sys.stderr.write('error: target dir is not empty. please remove all the files inside it\n')
        sys.exit(1)

    wiiu = args.target == 'wiiu'

    table = rstb.util.read_rstb(args.content_dir / _RSTB_PATH_IN_CONTENT, be=wiiu)

    make_loadable_layer(args.content_dir, args.patch_dir, args.target_dir, wiiu, table, is_aoc=False)
    if args.aoc_dir or args.aoc_patch_dir or args.aoc_target_dir:
        if args.aoc_dir and args.aoc_patch_dir and args.aoc_target_dir:
            make_loadable_layer(args.aoc_dir, args.aoc_patch_dir, args.aoc_target_dir, wiiu, table, is_aoc=True)
        else:
            sys.stderr.write('Not all aoc arguments were specified - ignoring aoc files\n')

    sys.stderr.write('writing new RSTB...\n')
    table.set_size(_RSTB_PATH_IN_CONTENT.replace('.srsizetable', '.rsizetable'), table.get_buffer_size())
    final_rstb_path = args.target_dir / _RSTB_PATH_IN_CONTENT
    os.makedirs(final_rstb_path.parent, exist_ok=True)
    rstb.util.write_rstb(table, str(final_rstb_path), be=wiiu)

if __name__ == '__main__':
    cli_main()
