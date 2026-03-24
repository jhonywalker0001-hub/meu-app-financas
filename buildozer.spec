[app]
title = Minhas Financas 2026
package.name = appfinancas
package.domain = org.jhonywalker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0

requirements = python3,kivy==2.2.1,kivymd==1.1.1,matplotlib,numpy,pandas,pytz,openpyxl,fpdf2,pillow,cycler,kiwisolver,pyparsing,python-dateutil,six

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 21
android.enable_androidx = True
android.archs = arm64-v8a
android.accept_sdk_license = True
android.gradle_options = org.gradle.jvmargs=-Xmx4096m

[buildozer]
log_level = 2
warn_on_root = 0
