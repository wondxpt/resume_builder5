[app]

title = Resume Builder
package.name = resumebuilder
package.domain = com.wondxpt

source.dir = .
version = 1.0.0

requirements = python3==3.11.7,kivy==2.3.0,kivymd==1.2.0,pillow,reportlab

source.include_exts = py,png,jpg,jpeg,kv,json,ttf,otf,txt

source.exclude_dirs = .git,.github,.buildozer,bin,p4a-recipes

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png

presplash.filename = %(source.dir)s/presplash.png

android.api = 34
android.minapi = 24

android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET

android.enable_androidx = True
android.copy_libs = 1

android.accept_sdk_license = True

android.debug_artifact = apk
android.release_artifact = aab

p4a.fork = kivy
p4a.branch = v2024.01.21

p4a.local_recipes = %(source.dir)s/p4a-recipes

[buildozer]

log_level = 2
warn_on_root = 1
