[app]

title = Resume Builder
package.name = resumebuilder
package.domain = org.wondxpt

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json

version = 1.0.0

requirements = python3==3.11.7,hostpython3==3.11.7,kivy==2.3.0,kivymd==1.2.0,pillow,reportlab

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

android.api = 35
android.minapi = 24
android.ndk = 28c
android.archs = arm64-v8a,armeabi-v7a

android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-sdk/ndk/28.0.13004108

android.accept_sdk_license = True
android.entrypoint = org.kivy.android.PythonActivity
android.enable_androidx = True

android.permissions = INTERNET

warn_on_root = 1
log_level = 2
