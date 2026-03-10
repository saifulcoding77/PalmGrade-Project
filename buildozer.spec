[app]
title = PalmGrade AI
package.name = palmgradeai
package.domain = org.palmgrade
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# REQUIREMENTS: Guna versi yang paling asas & stabil sahaja
requirements = python3,hostpython3,kivy==2.2.1,kivymd,android,pyjnius,openssl,requests,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 0

# PERMISSIONS
android.permissions = INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# SETTING VIVO V21 (64-bit)
android.ndk_path = 
android.sdk_path = 
android.ant_path =
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# KESTABILAN SISTEM
# Supaya aplikasi boleh akses hardware audio untuk Bunyi BEEP
android.allow_backup = True
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version
android.skip_update_buildozer = False
p4a.branch = stable

# Tambah ini untuk mengelakkan ralat 'stripping' pada binary
android.skip_update_buildozer = False

# (8) Log & Debug
log_level = 2
warn_on_root = 1






