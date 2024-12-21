import sys
import site

# Добавьте путь к библиотеке pydub, если она не находится в стандартных путях поиска
site.addsitedir(r'E:\PythonProject\m4a-to-mp3\.venv\Lib\site-packages')

# Обновленный .spec файл
a = Analysis(
    ['E:/PythonProject/m4a-to-mp3/main.py'],
    pathex=['.'],
    binaries=[
        (os.path.join(r'C:\ffmpeg', 'ffmpeg.exe'), '.'),
        (os.path.join(r'C:\ffmpeg', 'ffplay.exe'), '.'),
        (os.path.join(r'C:\ffmpeg', 'ffprobe.exe'), '.')
    ],
    datas=[],
    hiddenimports=['pydub', 'tqdm', 'customtkinter', 'colorama', 'yt_dlp', 'darkdetect', 'packaging'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='m4a-To-mp3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
