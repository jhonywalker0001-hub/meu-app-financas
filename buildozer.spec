[app]
title = Minhas Financas 2026
package.name = appfinancas
package.domain = org.jhonywalker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0

# SEM matplotlib por enquanto - só o essencial
requirements = python3,kivy==2.2.1,kivymd==1.1.1,fpdf2,openpyxl,pillow

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
