[app]
title = Financas 2026
package.name = financasapp
package.domain = org.jhonywalker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db,json
version = 1.0
requirements = python3,kivy==2.2.1,kivymd,openpyxl,fpdf2
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.local_recipes = 
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
[buildozer]
log_level = 2
warn_on_root = 0
