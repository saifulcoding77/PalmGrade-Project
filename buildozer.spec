[app]
title = PalmGrade AI
package.name = palmgradeai
package.domain = org.palmgrade
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 1. KEMASKINI REQUIREMENTS: Kita guna versi OpenCV yang lebih stabil
requirements = python3,kivy==2.2.1,numpy,opencv-python-headless,pillow,android

orientation = portrait
fullscreen = 0
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# 2. VERSI ANDROID: Vivo V21 perlukan API yang lebih tinggi
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# 3. SENIBINA (PENTING): Vivo V21 adalah 64-bit sepenuhnya
# Kita hanya bina untuk arm64-v8a supaya tidak 'confuse' sistem Funtouch OS
android.archs = arm64-v8a

# 4. TAMBAH SETTING GRAFIK:
android.allow_backup = True
p4a.branch = master
