[app]
title = Minhas Financas 2026
package.name = appfinancas
package.domain = org.jhonywalker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db
version = 1.0.0

# Adicionado pillow (essencial para KivyMD)
requirements = python3,kivy==2.2.1,kivymd==1.1.1,fpdf2,openpyxl,pillow

orientation = portrait
fullscreen = 0

# Adicionado permissões para salvar os relatórios PDF/Excel
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

# Dica: adicione armeabi-v7a para o app funcionar em celulares mais antigos também
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 0
