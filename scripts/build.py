import patch
import os
import contextlib
import subprocess
from pathlib import Path

patches = [
]


@contextlib.contextmanager
def working_directory(path):
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


#
# make depot_tools available
depot_tools_dir = Path('depot_tools').absolute().as_posix()
os.environ["PATH"] += os.pathsep + depot_tools_dir

#
# this adds "python3.bat" on win, else gn will fail
with working_directory('depot_tools'):
    subprocess.check_call(os.path.join('bootstrap', 'win_tools.bat'))

#
# download skia dependencies
with working_directory('skia'):
    subprocess.check_call(os.path.join('python tools', 'git-sync-deps'))

with working_directory('skia'):
    for path_file in patches:
        patch.fromfile(Path(path_file).as_posix()).apply()

with working_directory('skia'):
    args = [
        #
        # setup
        'is_official_build=true',  # this is recommended for optimization
        'skia_use_gl=false',  # don't need this anymore
        'skia_use_direct3d=true',  # replacement for gl on windows
        'skia_enable_svg=true',  # !
        'skia_enable_tools=true',  # ?
        #
        # no need:
        'skia_use_system_libjpeg_turbo=false',
        'skia_use_system_libwebp=false',
        'skia_use_system_libpng=false',
        'skia_use_system_icu=false',
        'skia_use_system_harfbuzz=false',
        'skia_use_system_expat=false',
        'skia_use_system_zlib=false',
        #
        # flags
        'extra_cflags_cc=["/GR", "/EHsc", "/MD"]'
    ]
    args = ' '.join(args)
    subprocess.check_call([
        os.path.join('bin', 'gn.exe'),
        'gen',
        'out/Release',
        f"--args={args}"
    ])

with working_directory('skia'):
    subprocess.check_call('ninja -C out/Release skia skia.h')
