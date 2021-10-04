# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
         ( r'C:\Users\SAI\Python_Scr\Kinopoisk\KinoPoiskAPI\searching.ico', '.' )
         ]
a = Analysis(['Film_searcher.py'],
             pathex=['C:\\Users\\SAI\\Python_Scr\\Kinopoisk\\KinoPoiskAPI'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='Film searcher',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='searching.ico')
