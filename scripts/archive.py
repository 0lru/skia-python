#! /usr/bin/env python3

import os
import pathlib
import sys
import zipfile
import platform

machine = {'AMD64': 'x64', 'x86_64': 'x64', 'arm64': 'arm64'}[platform.machine()]
system = {'Darwin': 'macos', 'Linux': 'linux', 'Windows': 'windows'}[platform.system()]
build_type = 'Release'


def parents(path):
    res = []
    parent = path.parent
    while '.' != str(parent):
        res.insert(0, parent)
        parent = parent.parent
    return res


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), os.pardir, 'skia'))

    globs = [
        'out/Release/*.a',
        'out/Release/*.lib',
        'out/Release/icudtl.dat',
        'third_party/externals/angle2/LICENSE',
        'third_party/externals/freetype/docs/FTL.TXT',
        'third_party/externals/freetype/docs/GPLv2.TXT',
        'third_party/externals/freetype/docs/LICENSE.TXT',
        'third_party/externals/libpng/LICENSE',
        'third_party/externals/libwebp/COPYING',
        'third_party/externals/libwebp/PATENTS',
        'third_party/externals/harfbuzz/COPYING',
        'third_party/externals/swiftshader/LICENSE.txt',
        'third_party/externals/zlib/LICENSE',
    ]

    target = f'skia_{system}_release_{machine}.zip'
    print('> writing', target)

    with zipfile.ZipFile(os.path.join(os.pardir, target), 'w', compression=zipfile.ZIP_DEFLATED) as zip:
        dirs = set()
        for glob in globs:
            for path in pathlib.Path().glob(glob):
                if not path.is_dir():
                    for dir in parents(path):
                        if not dir in dirs:
                            zip.write(str(dir))
                            dirs.add(dir)
                    zip.write(str(path))

    return 0


if __name__ == '__main__':
    sys.exit(main())
