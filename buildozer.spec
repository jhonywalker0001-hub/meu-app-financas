[app]
title = Financas2026
package.name = financasapp
package.domain = org.meuapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xlsx
version = 1.0.0
requirements = python3,kivy,pandas,openpyxl
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
