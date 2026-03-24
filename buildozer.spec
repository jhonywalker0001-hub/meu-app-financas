[app]

# (str) Título do seu aplicativo
title = Minhas Financas

# (str) Nome do pacote
package.name = appfinancas

# (str) Domínio do pacote
package.domain = org.meunome

# (str) Pasta onde está o seu main.py
source.dir = .

# (list) Extensões de arquivos para incluir no APK
source.include_exts = py,png,jpg,kv,atlas,db

# (str) Versão do aplicativo (Importante para não dar erro!)
version = 0.1

# (list) Requisitos do Aplicativo
# ADICIONADO: Matplotlib e todas as dependências que causavam erro
requirements = python3,kivy==2.2.1,kivymd==1.1.1,matplotlib,numpy,pandas,sqlite3,openpyxl,fpdf,pillow,cycler,kiwisolver,pyparsing,python-dateutil

# (list) Orientações suportadas
orientation = portrait

#
# Android specific
#

# (bool) Indica se o app será tela cheia
fullscreen = 0

# (list) Permissões do Android
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (int) API do Android (33 é ideal para o S25)
android.api = 33

# (int) API mínima suportada
android.minapi = 21

# (bool) Ativa o suporte AndroidX (Obrigatório para KivyMD)
android.enable_androidx = True

# (list) Arquiteturas para o S25 e celulares modernos
android.archs = arm64-v8a, armeabi-v7a

# (bool) Ativa backup automático
android.allow_backup = True

[buildozer]

# (int) Nível de Log (2 mostra tudo o que está acontecendo)
log_level = 2

# (int) Aviso se rodar como root
warn_on_root = 1
