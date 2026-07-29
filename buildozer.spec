[app]

# (str) Title of your application
title = Resume Builder

# (str) Package name
package.name = resumebuilder

# (str) Package domain
package.domain = org.wondxpt

# (str) Source code directory
source.dir = .

# (str) Application entry point
source.main = main.py

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,otf,pdf

# (list) Python requirements
requirements = python3==3.11.7,hostpython3==3.11.7,kivy==2.3.0,kivymd==1.2.0,pillow,reportlab

# (str) Presplash
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation
orientation = portrait

# (str) Android API
android.api = 34

# (str) Minimum Android API
android.minapi = 24

# (str) Android NDK version
android.ndk = 25b

# (str) Android architecture
android.archs = arm64-v8a, armeabi-v7a

# (bool) Fullscreen
fullscreen = 0

# (str) Android permissions
android.permissions = INTERNET

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.presplash_color = #FFFFFF

# (bool) Copy libraries
android.copy_libs = 1

# (str) Python-for-Android release channel
p4a.channel = stable

# (str) Log level
log_level = 2

# (bool) Warn when running as root
warn_on_root = 1


[buildozer]

# (str) Log level
log_level = 2

# (str) Warning when running as root
warn_on_root = 1
