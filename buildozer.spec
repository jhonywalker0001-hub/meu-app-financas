[app]
title = Financas 2026
package.name = financasapp
package.domain = org.jhonywalker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db,json,xlsx,xls,pdf,csv
version = 1.0.0

# REQUIREMENTS: Removi o sqlite3 daqui pois ele ja vem no python3 do p4a
requirements = python3,kivy==2.2.1,kivymd,numpy,pandas,pytz,openpyxl,fpdf2

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Ajuste para evitar o aviso vermelho: usamos apenas o api
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.private_storage = True
android.accept_sdk_license = True
android.entrypoint = main.py
android.archs = arm64-v8a, armeabi-v7a

# O caminho do Java deve ser exatamente este no GitHub Actions
android.java_home = /opt/hostedtoolcache/Java_Temurin-Hotspot_jdk/17.0.18-8/x64

[buildozer]
log_level = 2
warn_on_root = 0
bin_dir = ./bin
