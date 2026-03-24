[app]
title = Minhas Finanças
package.name = financas
package.domain = org.jhony
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,ttf
version = 1.0

# Requisitos corrigidos e estáveis (2026)
requirements = python3,kivy==2.2.1,kivymd==1.2.0,matplotlib,pillow,sqlite3

orientation = portrait
fullscreen = 0

# Android configurações
android.permissions = INTERNET
android.api = 34
android.minapi = 21
p4a.bootstrap = sdl2
p4a.branch = master

# Acelera a build
buildozer.version = master
