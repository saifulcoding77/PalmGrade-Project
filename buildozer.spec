[app]
title = PalmGrade AI
package.name = palmgradeai
package.domain = org.palmgrade
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Keperluan Pustaka -opencv-python-headless adalah wajib untuk Android
requirements = python3,kivy==2.2.1,numpy,opencv-python-headless

orientation = portrait
fullscreen = 0
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# Versi Android
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# Seni Bina (arm64 untuk telefon moden)
android.archs = arm64-v8a

# Tetapan Kestabilan GitHub
p4a.branch = master
android.accept_sdk_license = True
android.skip_update = False



