[app]

(str) Title of your application

title = Resume Builder

(str) Package name

package.name = resumebuilder

(str) Package domain

package.domain = org.wondxpt

(str) Source code directory

source.dir = .

(str) Application version

version = 1.0.0

(str) Supported file extensions

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,otf

(list) List of inclusions using pattern matching

source.include_patterns = assets/,fonts/

(str) Application requirements

requirements = python3==3.11.7,kivy==2.3.0,kivymd==1.2.0,pillow,reportlab

(str) Presplash

presplash.filename = %(source.dir)s/presplash.png

(str) Icon

icon.filename = %(source.dir)s/icon.png

(str) Orientation

orientation = portrait

(str) Android API

android.api = 35

(str) Minimum Android API

android.minapi = 24

(str) Android NDK version

android.ndk = 25b

(str) Android architectures

android.archs = arm64-v8a,armeabi-v7a

(str) Android app theme

android.entrypoint = org.kivy.android.PythonActivity

(bool) Fullscreen

fullscreen = 0

(str) Python-for-Android branch

p4a.branch = master

(str) Android permissions

android.permissions = INTERNET

(str) Android private storage

android.private_storage = True

(str) Android release build

android.release_artifact = apk

(str) Android debug build

android.debug_artifact = apk

(str) Log level

log_level = 2

[buildozer]

(str) Log level

log_level = 2

(str) Warning for root user

warn_on_root = 1

(str) Build directory

build_dir = .buildozer

(str) Android SDK/NDK packages directory

bin_dir = bin
