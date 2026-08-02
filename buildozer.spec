[app]
title = Resume Builder
package.name = resumebuilder
package.domain = com.wondxpt

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json

version = 1.0.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,fpdf2,pillow==10.4.0,plyer

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

android.api = 34
android.minapi = 24
android.ndk = 25c
android.ndk_api = 24

android.archs = arm64-v8a,armeabi-v7a

android.permissions = READ_MEDIA_IMAGES,READ_EXTERNAL_STORAGE

android.enable_androidx = True
android.accept_sdk_license = True
android.presplash_color = #FFFFFF

p4a.branch = master
p4a.commit = 957a3e5

[buildozer]
log_level = 2
warn_on_root = 1
recipe.freetype.url
