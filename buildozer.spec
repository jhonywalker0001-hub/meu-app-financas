[app]
title = Minhas Finanças
package.name = financas
package.domain = org.jhony
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,ttf
version = 1.0

requirements = python3,kivy==2.3.0,https://github.com/kivymd/KivyMD/archive/master.zip,matplotlib,pillow,sqlite3

orientation = portrait
fullscreen = 0

# Android
android.permissions = INTERNET
android.api = 34
android.minapi = 21
p4a.bootstrap = sdl2
p4a.branch = master

# Melhor performance na build
buildozer.version = master
