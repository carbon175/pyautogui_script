# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['insect_sheep.py'],
    pathex=[],
    binaries=[],
    datas=[('whistle_sheep.png', '.'), ('ball_sheep.png', '.'), ('turn_sheep.png', '.'), ('beetle_sheep.png', '.'), ('candy_sheep.png', '.'), ('war_sheep.png', '.'), ('bug1_sheep.png', '.'), ('bug2_sheep.png', '.'), ('bug3_sheep.png', '.'), ('bug4_sheep.png', '.'), ('bug5_sheep.png', '.'), ('bug6_sheep.png', '.')],
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
    name='insect_sheep',
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
