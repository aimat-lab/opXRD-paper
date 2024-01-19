# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['run/prod_run.py'],
    pathex=['/home/daniel/aimat/datapaper'],
    binaries=[],
    datas=[
    ('/home/daniel/aimat/datapaper/data_collector/resources/images/*', 'images'),  # Include all files in the 'images' directory
    ('/home/daniel/aimat/datapaper/data_collector/resources/documents/*', 'documents'),  # Include all files in the 'documents' directory
],
    hiddenimports=['python-intervals'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='prod_run',
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
