# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['insect_chia.py'],
    pathex=[],
    binaries=[],
    datas=[('whistle_chia.png', '.'), ('ball_chia.png', '.'), ('turn_chia.png', '.'), ('beetle_chia.png', '.'), ('candy_chia.png', '.'), ('war_chia.png', '.'), ('bug1_chia.png', '.'), ('bug2_chia.png', '.'), ('bug3_chia.png', '.'), ('bug4_chia.png', '.'), ('power_bar_60_chia.png', '.'), ('bug5_chia.png', '.'), ('bug6_chia.png', '.')],
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
    name='insect_chia',
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
