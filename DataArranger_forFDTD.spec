# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Python/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('DataArranger_forFDTD', 'DataArranger_forFDTD'),
        ('DataArranger_forFDTDContent', 'DataArranger_forFDTDContent'),
        ('DataArranger_forFDTDContent/images', 'DataArranger_forFDTDContent/images')
    ],
    hiddenimports=[
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuickControls2',
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGraphs'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pip', 'img2pdf', 'matplotlib', 'matplotlib-inline', 'pyinstaller', 'pyinstaller-hooks-contrib', 'tqdm', 'setuptools'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DataArranger_forFDTD',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DataArranger_forFDTD',
)
app = BUNDLE(
    coll,
    name='DataArranger_forFDTD.app',
    icon=None,
    bundle_identifier=None,
)
