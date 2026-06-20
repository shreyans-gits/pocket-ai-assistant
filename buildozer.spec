[app]
title = ZORO
package.name = zoro
package.domain = org.shreyans
icon.filename = assets/logo.png
presplash.filename = assets/logo.png

source.dir = .
source.include_exts = py,png,jpg,kv,txt,json,ini

version = 1.0.0

requirements = python3,kivy==2.2.1,kivymd==1.2.0,groq,python-dotenv,requests,plyer,edge-tts,pygame,speechrecognition,certifi,idna,sniffio,anyio,httpx,httpcore,h11

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, RECORD_AUDIO, READ_CONTACTS, CALL_PHONE, SEND_SMS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
android.manifest.application.usesCleartextTraffic = true

p4a.branch = v2024.01.21
# DO NOT add p4a.commit — the tag is enough

android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1