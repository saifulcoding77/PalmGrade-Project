[app]
# (Nama Aplikasi)
title = PalmGrade AI
# (Nama Pakej - Huruf kecil sahaja)
package.name = palmgradeai
# (Domain organisasi anda)
package.domain = org.palmgrade

# (Lokasi kod utama)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# (Keperluan Pustaka - Kita gunakan Kivy sahaja dahulu untuk kestabilan di GitHub)
requirements = python3,kivy==2.2.1,numpy,pillow

# (Tetapan Skrin)
orientation = portrait
fullscreen = 0

# (Kebenaran Android - Penting untuk Kamera & Simpan Data)
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (Versi Android - Standard 2026)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# (Seni Bina Pemproses - arm64 adalah wajib untuk telefon moden)
android.archs = arm64-v8a

# (Pilihan Tambahan)
p4a.branch = master