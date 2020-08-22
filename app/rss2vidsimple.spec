# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

block_cipher = None


a = Analysis(['..\\src\\main.py'],
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn', 'plyer.platforms.win.filechooser'],
             hookspath=[kivymd_hooks_path],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz, Tree('..\\',
          excludes=['*.mp3', '*.mkv', '*.spec', '*.png', '*.jpg', 'ffmpeg.exe', 'assets']),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='rss2vidsimple',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='C:\\Users\\arman\\PycharmProjects\\rss_video_app\\assets\\icon.ico')

import shutil
shutil.copyfile('C:\\Users\\arman\\PycharmProjects\\rss_video_app\\samples\\mic.jpg',
                '{0}\\mic.jpg'.format(DISTPATH))
shutil.copyfile('C:\\Users\\arman\\PycharmProjects\\rss_video_app\\icon.png',
                '{0}\\icon.png'.format(DISTPATH))
shutil.copyfile('C:\\Users\\arman\\PycharmProjects\\rss_video_app\\ffmpeg.exe',
                '{0}\\ffmpeg.exe'.format(DISTPATH))
shutil.copyfile('..\\assets\\ffmpeg-snapshot.tar.bz2',
                '{0}\\ffmpeg-snapshot.tar.bz2'.format(DISTPATH))
shutil.copyfile('C:\\Users\\arman\\PycharmProjects\\rss_video_app\\LICENSE',
                '{0}\\LICENSE'.format(DISTPATH))
