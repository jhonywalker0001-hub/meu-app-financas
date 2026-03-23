[app]

# (section) Title of your application
title = Financas 2026

# (section) Package name
package.name = financasapp

# (section) Package domain (needed for android packaging)
package.domain = org.jhonywalker

# (section) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,db,json,xlsx,xls,pdf,csv

# (list) Application requirements
# Adicionado numpy, pandas, pytz e sqlite3 para garantir a lógica de finanças
requirements = python3,kivy==2.2.1,kivymd,numpy,pandas,pytz,openpyxl,fpdf2,sqlite3

# (str) Custom source folders for requirements
# android.add_src = 

# (list) Permissions
# Permissões essenciais para escrita de arquivos e banco de dados no Android moderno
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (leave empty to download)
android.ndk_path = 

# (str) Android SDK directory (leave empty to download)
android.sdk_path = 

# (str) ANT directory (leave empty to download)
android.ant_path = 

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# Isso evita travamentos no terminal do GitHub Actions
android.accept_sdk_license = True

# (str) Android entry point, default is main.py
android.entrypoint = main.py

# (list) Android application meta-data
android.meta_data = 

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Path to a custom whitelist file
# android.whitelist = 

# (str) Path to JAVA_HOME (CRÍTICO PARA TENTATIVA 96)
# Força o Buildozer a usar o caminho exato do Java 17 no GitHub Actions
android.java_home = /opt/hostedtoolcache/Java_Temurin-Hotspot_jdk/17.0.18-8/x64

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 0

# (str) Path to build artifact storage, default is ./bin
bin_dir = ./bin
