[app]
title = Minhas Finanças
package.name = financas
package.domain = org.jhony
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0

requirements = python3,kivy==2.3.0,kivymd==2.0.1.dev0,matplotlib,pillow

orientation = portrait
fullscreen = 0

# Para acelerar a build (importante!)
android.permissions = INTERNET
android.api = 33
android.minapi = 21
p4a.branch = master
p4a.bootstrap = sdl2

# Se você usa matplotlib, pode precisar disso:
osx.python_version = 3.10
