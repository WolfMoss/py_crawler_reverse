# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['slider_validation.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('stealth.min.js', '.'),
    ('page.js', '.'),
    ('dl.PNG', '.'),
    ('hk.PNG', '.'),
    (r'E:\codes\Python\Python310\Lib\site-packages\playwright\driver','playwright/driver')
    ],
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
    name='slider_validation',
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
