# -*- mode: python -*-

block_cipher = None


a = Analysis(['flash.py'],
             pathex=['C:\\Users\\Animcogn\\github\\esp32-mongoose-flash\\python'],
             binaries=[('mos.exe', '.'), ('esptool.exe', '.')],
             datas=[('firmware', '.')],
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
          name='flash',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
