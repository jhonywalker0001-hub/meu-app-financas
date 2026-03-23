[app]
title = Financas2026
package.name = financasapp
package.domain = org.jhony
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db,xlsx
version = 1.0.0

# REQUISITOS ATUALIZADOS: Adicionei kivymd, matplotlib, fpdf2 e numpy
requirements = python3,kivy==2.2.1,kivymd,sqlite3,pandas,openpyxl,matplotlib,fpdf2,numpy

orientation = portrait
fullscreen = 0

# PERMISSÕES: Adicionei MANAGE_EXTERNAL_STORAGE para o Android 13+
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
