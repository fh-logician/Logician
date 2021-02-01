# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None

a = Analysis(['main.py'],
             pathex=['/Users/fellowhashbrown/Desktop/Developing/Python/Projects/Logician'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Logician',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon="logician.ico" if sys.platform != "darwin" else "logician.icns")

# The app to build if on a Windows or Linux machine
if sys.platform == "win32" or sys.platform == "win64" or sys.platform == "linux":
    app = BUNDLE(exe,
                 name='Logician.exe')

# The app to build if on a MacOS machine
if sys.platform == "darwin":
    app = BUNDLE(exe,
                 name="Logician.app",
                 icon="logician.icns",
                 info_plist = {
                    "NSHighResolutionCapable": "True",
                    "CFBundleVersion": "0.1.2",
                    "CFBundleShortVersionString": "0.1.2"
                 },
                 bundle_identifier=None)
