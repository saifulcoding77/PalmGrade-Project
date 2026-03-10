[app]
title = PalmGrade AI
package.name = palmgradeai
package.domain = org.palmgrade
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# REQUIREMENTS: Hostpython3 sangat penting untuk kestabilan di GitHub
requirements = python3,hostpython3,kivy==2.2.1,kivymd,android,pyjnius,openssl,requests,urllib3,certifi

orientation = portrait
fullscreen = 0

# PERMISSIONS
android.permissions = INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# SETTING VIVO V21 (API 33 adalah yang paling stabil di GitHub sekarang)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# KESTABILAN SISTEM
p4a.branch = stable
log_level = 2
