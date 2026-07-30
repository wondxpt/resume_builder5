[app]

# (str) Title of your application
title = Resume Builder

# (str) Package name
package.name = resumebuilder

# (str) Package domain
package.domain = org.resumebuilder

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,ttf,otf,woff,woff2

# (list) Source directories to exclude
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__

# (list) Source patterns to exclude
source.exclude_patterns = *.pyc,*.pyo,.git/*,.github/*,.buildozer/*,bin/*

# (str) Application version
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,reportlab

# (str) Custom orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# (str) Presplash
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon
# icon.filename = %(source.dir)s/data/icon.png


#
# Android
#

# (bool) Enable Android
android.enable_androidx = True

# Android API
android.api = 35

# Minimum Android API
android.minapi = 24

# Android NDK
android.ndk = 25b

# Android architectures
android.archs = arm64-v8a,armeabi-v7a

# Android permissions
android.permissions = INTERNET

# Android private storage
android.private_storage = True

# Android orientation
android.orientation = portrait

# Android backup
android.allow_backup = False

# Android numeric version
android.numeric_version = 1


#
# Python-for-Android
#

# Use the installed/pinned python-for-android package.
# Do not use a custom local recipe in this build.
p4a.fork = kivy

# Keep p4a on the stable 2024 release installed by build.yml.
# Do not add p4a.local_recipes here.


#
# Buildozer
#

# Log level
log_level = 2

# Warn if running as root
warn_on_root = 1

# Build directory
build_dir = ./.buildozer

# Output directory
bin_dir = ./bin
