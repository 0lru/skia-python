import patch
import os
import contextlib
import subprocess
from pathlib import Path

patches = [
    '../patch/make_data_assembly.patch'
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
# download skia dependencies
with working_directory('skia'):
    subprocess.check_call(os.path.join('python tools', 'git-sync-deps'))

with working_directory('skia'):
    for path_file in patches:
        patch.fromfile(Path(path_file).as_posix()).apply()

with working_directory('skia'):
    args = [
        'is_official_build=true',
        'skia_enable_tools=true',
        'skia_use_system_libjpeg_turbo=false',
        'skia_use_system_libwebp=false',
        'skia_use_system_libpng=false',
        'skia_use_system_icu=false',
        'skia_use_system_harfbuzz=false',
        'skia_use_system_expat=false',
        'skia_use_system_zlib=false',
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
    subprocess.check_call('ninja -C out/Release skia skia.h experimental_svg_model')
