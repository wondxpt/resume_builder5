[app]

# (str) Title of your application
title = Resume Builder

# (str) Package name
package.name = resumebuilder

# (str) Package domain
package.domain = com.wondxpt

# (str) Source code directory
source.dir = .

# (str) Main entry point
source.main = main.py

# (list) Application requirements
requirements = python3==3.11.7,kivy==2.3.0,kivymd==1.2.0,pillow,reportlab

# (str) Application version
version = 1.0.0

# (list) Supported orientations
orientation = portrait

# (str) Icon
icon.filename = %(source.dir)s/icon.png

# (str) Presplash
presplash.filename = %(source.dir)s/presplash.png

# (list) Include these file extensions
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json

# (str) Application startup mode
fullscreen = 0

# (str) Android application name
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.apptheme = @android:style/Theme.Material.Light.NoActionBar

# (str) Android API
android.api = 34

# (str) Android minimum API
android.minapi = 24

# (str) Android NDK version
android.ndk = 25b

# (str) Android NDK API
android.ndk_api = 24

# (str) Android architectures
android.archs = arm64-v8a,armeabi-v7a

# (str) Android permissions
android.permissions = INTERNET

# (bool) Copy libraries
android.copy_libs = 1

# (str) Android accept SDK licenses
android.accept_sdk_license = True

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (bool) Android backup
android.allow_backup = False

# (str) Android package source
android.add_src =

# (str) Android extra Java classes
android.add_src_jars =

# (str) Android extra AARs
android.add_aars =

# (str) Android extra Gradle repositories
android.gradle_repositories =

# (str) Android extra Gradle dependencies
android.gradle_dependencies =

# (str) Android whitelist source
android.whitelist_src =

# (str) Android whitelist recipes
android.whitelist_recipe =

# (str) Android private storage
android.private_storage = True

# (str) Android activity class
android.activity_class_name = org.kivy.android.PythonActivity

# (str) Android app category
android.category = APPLICATION

# (str) Android service
services =

# (str) Python-for-Android branch
p4a.branch = master

# (str) Python-for-Android commit
p4a.commit =

# (str) Python-for-Android fork
p4a.fork =

# (str) Android SDK directory
android.sdk_path =

# (str) Android NDK directory
android.ndk_path =

# (str) Build directory
build_dir = .buildozer

# (str) Output directory
bin_dir = bin

# (bool) Warn when running as root
warn_on_root = 1


[buildozer]

# (int) Log level
log_level = 2

# (str) Build warnings
warn_on_root = 1
