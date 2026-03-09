[app]

# (1) Maklumat Asas
title = PalmGrade AI
package.name = palmgrade
package.domain = org.manager.sawit
# TAMBAHKAN BARISAN INI:
version = 0.1

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# (2) Keperluan Pustaka (PENTING!)
# Pastikan ada openssl dan requests untuk Google Sheets Sync
requirements = python3,kivy==2.2.1,android,pyjnius,openssl,requests,urllib3,certifi

# (3) Kebenaran Android (Permissions)
# Wajib ada untuk Kamera, Internet, dan Storan Offline
android.permissions = INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# (4) Versi Android (Target Vivo V21)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# (5) Seni Bina Pemproses (Wajib untuk Vivo moden)
android.archs = arm64-v8a, armeabi-v7a

# (6) Orientasi & Skrin
orientation = portrait
fullscreen = 0

# (7) Ciri Tambahan Android
# Supaya aplikasi boleh akses hardware audio untuk Bunyi BEEP
android.allow_backup = True
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# (8) Log & Debug
log_level = 2
warn_on_root = 1

