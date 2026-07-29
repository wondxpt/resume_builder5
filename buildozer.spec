[app]

# نام برنامه
title = Resume Builder

# نام پکیج
package.name = resumebuilder

# دامنه پکیج
package.domain = org.wondxpt

# مسیر فایل‌های برنامه
source.dir = .

# پسوندهایی که همراه برنامه قرار می‌گیرند
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json

# نسخه برنامه
version = 1.0.0

# کتابخانه‌های مورد نیاز
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,reportlab

# جهت صفحه
orientation = portrait

# نمایش تمام‌صفحه
fullscreen = 0


# --------------------------------------------------
# Android
# --------------------------------------------------

# حداقل نسخه Android
android.minapi = 24

# Android API مورد استفاده برای Build
android.api = 35

# معماری‌ها
android.archs = arm64-v8a,armeabi-v7a

# NDK
android.ndk = 28c

# مسیر SDK
android.sdk_path = /home/runner/android-sdk

# قبول License
android.accept_sdk_license = True


# --------------------------------------------------
# Android application settings
# --------------------------------------------------

# نام Activity
android.entrypoint = org.kivy.android.PythonActivity

# AndroidX
android.enable_androidx = True

# اجازه دسترسی اینترنت
android.permissions = INTERNET


# --------------------------------------------------
# Build settings
# --------------------------------------------------

# هشدارهای Buildozer
warn_on_root = 1

# خروجی لاگ
log_level = 2
