[app]
title = PalmGrade AI
package.name = palmgradeai
package.domain = org.palmgrade
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# REQUIREMENTS: Guna versi yang paling asas & stabil sahaja
requirements = python3,kivy==2.2.1,android

orientation = portrait
fullscreen = 0

# PERMISSIONS
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# SETTING VIVO V21 (64-bit)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# KESTABILAN SISTEM
android.allow_backup = True
android.skip_update_buildozer = False
p4a.branch = master


