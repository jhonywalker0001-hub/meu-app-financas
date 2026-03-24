[app]

# Nome do app
title = Minhas Finanças

# Nome do pacote (não pode ter espaço nem caracteres especiais)
package.name = financas
package.domain = org.jhony

# Diretório fonte
source.dir = .

# Arquivos que serão incluídos
source.include_exts = py,png,jpg,jpeg,kv,ttf

# Versão do app
version = 1.0

# Requisitos (mantenha versões estáveis)
requirements = python3,kivy==2.3.0,kivymd==2.0.1.dev0,matplotlib,pillow,sqlite3

# Orientação
orientation = portrait

# Permissões Android
android.permissions = INTERNET

# Versões do Android
android.api = 34
android.minapi = 21

# Acelera a build
p4a.branch = master
buildozer.branch = master

# Outras configurações úteis
fullscreen = 0
android.release = false
