[app]

title = Resume Builder
package.name = resumebuilder
package.domain = com.wondxpt

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf

version = 1.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,reportlab,pillow,plyer,android

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

[android]

android.api = 35
android.minapi = 24
android.ndk = 25b
p4a.branch = 2024.01.21

android.archs = arm64-v8a, armeabi-v7a

android.permissions = READ_MEDIA_IMAGES, READ_EXTERNAL_STORAGE

android.presplash_color = #FFFFFF

android.enable_androidx = True

android.accept_sdk_license = True


[buildozer]
log_level = 2
warn_on_root = 1
