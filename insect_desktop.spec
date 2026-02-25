# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['insect_desktop.py'],
    pathex=[],
    binaries=[],
    datas=[('whistle_desktop.png', '.'), ('ball_desktop.png', '.'), ('turn_desktop.png', '.'), ('beetle_desktop.png', '.'), ('candy_desktop.png', '.'), ('war_desktop.png', '.'), ('bug1_desktop.png', '.'), ('bug2_desktop.png', '.'), ('bug3_desktop.png', '.'), ('bug4_desktop.png', '.'), ('power_bar_60_desktop.png', '.'), ('bug5_desktop.png', '.'), ('bug6_desktop.png', '.')],
    hiddenimports=[],
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
    name='insect_desktop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
