# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['news_run.py',
    'GUI_CREATE.py',
    'Game.py',
    'NewsScraper.py'],
    pathex=[],
    binaries=[],
    datas=[('vedio/结束动画.mp4','vedio'),('vedio/myop.mp4','vedio'),('img/bkg.png','img'),('img/主背景.png','img')],
    hiddenimports=['jieba.posseg'],
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
    [],
    exclude_binaries=True,
    name='news_run',
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='news_run',
)
