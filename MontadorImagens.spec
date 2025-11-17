# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['montador_imagens.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'PIL', 'reportlab', 'reportlab.pdfgen', 'reportlab.lib.pagesizes', 'reportlab.lib.units'],
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
    name='MontadorImagens',
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
