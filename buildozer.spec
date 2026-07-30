[app]

title = Resume Builder
package.name = resumebuilder
package.domain = com.wondxpt

source.dir = .
source.main = main.py

version = 1.0.0

requirements = python3==3.11.7,kivy==2.3.0,kivymd==1.2.0,pillow,reportlab==4.0.9

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json

android.entrypoint = org.kivy.android.PythonActivity

android.api = 35
android.minapi = 24

android.ndk = 28c
android.ndk_api = 24

android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-sdk/ndk/28.0.13004108

android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET

android.copy_libs = 1
android.allow_backup = False
android.private_storage = True

android.logcat_filters = *:S python:D
android.category = APPLICATION

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
