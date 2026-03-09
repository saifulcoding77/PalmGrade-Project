import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from kivy.graphics import Color, Line
from kivy.metrics import dp  # Menggunakan dp untuk saiz yang konsisten pada pelbagai skrin

# Import fungsi Android untuk Bunyi dan Intent
if platform == 'android':
    from jnius import autoclass
    try:
        ToneGenerator = autoclass('android.media.ToneGenerator')
        AudioManager = autoclass('android.media.AudioManager')
        tone_gen = ToneGenerator(AudioManager.STREAM_ALARM, 100)
    except Exception as e:
        print(f"Ralat ToneGenerator: {e}")

class PalmGradeApp(App):
    def build(self):
        # 1. Inisialisasi Storan
        self.config_store = JsonStore('admin_config.json')
        self.offline_db = JsonStore('offline_data.json')
        
        if not self.config_store.exists('settings'):
            self.config_store.put('settings', url='', id_loc='', id_tot='', id_msk='', id_mkl='', id_mda='', id_cat='')
        
        self.count = {"Masak": 0, "Mengkal": 0, "Muda": 0, "Total": 0}
        self.is_waiting_for_relai = False

        # 2. Layout Utama (Padding ditingkatkan untuk keselesaan)
        self.layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Header & Status (Saiz teks dibesarkan)
        self.status_bar = Label(text="PALMGRADE READY", size_hint_y=None, height=dp(40), font_size='22sp', bold=True)
        self.layout.add_widget(self.status_bar)
        
        # Kamera & Target Box (Kamera dikecilkan sedikit untuk beri ruang pada butang)
        self.cam = Camera(play=True, resolution=(640, 480), allow_stretch=True, size_hint=(1, 0.35))
        with self.cam.canvas.after:
            Color(1, 0, 0, 1) # Merah supaya lebih nampak
            # Kotak target dibesarkan (150x150)
            self.target_box = Line(rectangle=(0, 0, 150, 150), width=dp(3))
        self.cam.bind(size=self.update_target_box, pos=self.update_target_box)
        self.layout.add_widget(self.cam)
        
        # Papan Markah (SCOREBOARD - Sangat Besar, warna Kuning untuk kontra)
        self.score_board = Label(text="Tundun: 0 | Masak: 0", size_hint_y=None, height=dp(60), color=(1, 1, 0, 1), font_size='32sp', bold=True)
        self.layout.add_widget(self.score_board)

        # Input Lokasi (Dikecilkan suapaya tidak ganggu butang greding)
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(5))
        self.txt_lokasi = TextInput(text='Lokasi', multiline=False, font_size='18sp', size_hint_x=0.4)
        self.txt_catatan = TextInput(text='Catatan', multiline=False, font_size='18sp', size_hint_x=0.6)
        input_layout.add_widget(self.txt_lokasi)
        input_layout.add_widget(self.txt_catatan)
        self.layout.add_widget(input_layout)
        
        # 3. BUTANG GRADING UTAMA (Sangat Besar & Tinggi)
        # Butang Sahkan Relai (MPOB) - Warna Hijau Pekat, Tinggi 100dp
        self.btn_relai = Button(text="SAHKAN MASAK (RELAY)", size_hint_y=None, height=dp(100), background_color=(0.1, 0.7, 0.1, 1), bold=True, font_size='28sp')
        self.btn_relai.bind(on_press=self.confirm_masak)
        self.layout.add_widget(self.btn_relai)

        # 4. Barisan Butang Aksi (Simpan, Sync, Reset - Sederhana Besar)
        action_bar = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(10))
        btn_save = Button(text="SIMPAN", background_color=(0.1, 0.5, 0.8, 1), bold=True, font_size='20sp')
        btn_save.bind(on_press=self.simpan_tempatan)
        
        btn_sync = Button(text="SYNC", background_color=(0.8, 0.6, 0.1, 1), bold=True, font_size='20sp')
        btn_sync.bind(on_press=self.sync_ke_cloud)
        
        btn_reset = Button(text="RESET", background_color=(0.6, 0.1, 0.1, 1), bold=True, font_size='20sp')
        btn_reset.bind(on_press=self.reset_count)
        
        action_bar.add_widget(btn_save)
        action_bar.add_widget(btn_sync)
        action_bar.add_widget(btn_reset)
        self.layout.add_widget(action_bar)

        # 5. Butang Admin (Kecil di bawah sekali, warna malap)
        btn_admin = Button(text="ADMIN", size_hint_y=None, height=dp(35), background_color=(0.2, 0.2, 0.2, 1), font_size='14sp')
        btn_admin.bind(on_press=self.show_password_popup)
        self.layout.add_widget(btn_admin)

        Clock.schedule_interval(self.auto_analyze, 0.3)
        return self.layout

    # --- LOGIK SISTEM ---
    def update_target_box(self, *args):
        cx, cy = self.cam.center
        # Kotak target dibesarkan (150x150)
        self.target_box.rectangle = (cx - 75, cy - 75, 150, 150)

    def play_beep(self, tone_type='BEEP'):
        if platform == 'android':
            try:
                t = ToneGenerator.TONE_PROP_BEEP if tone_type == 'BEEP' else ToneGenerator.TONE_PROP_ACK
                tone_gen.startTone(t)
            except: pass

    def auto_analyze(self, dt):
        if not self.cam.texture: return
        try:
            pixels = self.cam.texture.get_region(int(self.cam.texture.width/2), int(self.cam.texture.height/2), 1, 1).pixels
            r, g = pixels[0], pixels[1]
            if r > 160 and g < 110: 
                self.status_bar.text = "MASAK! TEKAN BUTANG BESAR!"
                self.status_bar.color = (0, 1, 0, 1) # Hijau
                self.is_waiting_for_relai = True
            else:
                self.status_bar.color = (1, 1, 1, 1) # Putih
                self.is_waiting_for_relai = False
        except: pass

    def confirm_masak(self, instance):
        if self.is_waiting_for_relai:
            self.count["Masak"] += 1
            self.count["Total"] += 1
            self.play_beep('BEEP')
            self.kemaskini_papan()
            # Tukar warna status sebentar untuk pengesahan visual
            self.status_bar.text = "REKODED!"
            Clock.schedule_once(lambda dt: self.reset_status(), 1)

    def reset_status(self):
        self.status_bar.text = "PALMGRADE READY"
        self.status_bar.color = (1, 1, 1, 1)

    def simpan_tempatan(self, instance):
        if self.count['Total'] == 0:
            self.status_bar.text = "Tiada data untuk disimpan!"
            return
        ts = time.strftime("%Y%m%d_%H%M%S")
        self.offline_db.put(ts, lokasi=self.txt_lokasi.text, total=self.count['Total'], 
                            masak=self.count['Masak'], catatan=self.txt_catatan.text)
        self.play_beep('ACK')
        self.status_bar.text = f"SIMPAN OFFLINE ({len(self.offline_db)})"
        self.reset_count(None)

    def sync_ke_cloud(self, instance):
        s = self.config_store.get('settings')
        if not s['url'] or len(self.offline_db) == 0:
            self.status_bar.text = "Tiada data/URL tidak sah!"
            return
        
        self.status_bar.text = "Sedang Sync..."
        for key in self.offline_db.keys():
            d = self.offline_db.get(key)
            params = {s['id_loc']: d['lokasi'], s['id_tot']: str(d['total']), s['id_msk']: str(d['masak']), s['id_cat']: d['catatan']}
            UrlRequest(s['url'], req_body=params, on_success=lambda r, v, k=key: self.on_sync_success(k), on_error=self.on_sync_error)

    def on_sync_success(self, key):
        self.offline_db.delete(key)
        self.status_bar.text = f"Sync Berjaya! Baki: {len(self.offline_db)}"

    def on_sync_error(self, req, error):
        self.status_bar.text = "Ralat Sync! Cek Internet."

    def kemaskini_papan(self):
        self.score_board.text = f"Tundun: {self.count['Total']} | Masak: {self.count['Masak']}"

    def reset_count(self, instance):
        for k in self.count: self.count[k] = 0
        self.kemaskini_papan()
        self.status_bar.text = "Kiraan Reset."

    # --- ADMIN PANEL ---
    def show_password_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.pwd = TextInput(password=True, multiline=False, hint_text="Password Admin", font_size='18sp')
        btn = Button(text="MASUK", size_hint_y=None, height=dp(50), font_size='20sp', bold=True)
        btn.bind(on_press=self.check_pwd)
        content.add_widget(self.pwd); content.add_widget(btn)
        self.pop = Popup(title="Admin Login", content=content, size_hint=(0.8, 0.4)); self.pop.open()

    def check_pwd(self, instance):
        if self.pwd.text == "admin123":
            self.pop.dismiss(); self.open_admin()
        else: self.status_bar.text = "Password Salah!"

    def open_admin(self):
        s = self.config_store.get('settings')
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        self.in_url = TextInput(text=s['url'], hint_text="URL Google Form Response", font_size='16sp')
        self.in_id_loc = TextInput(text=s['id_loc'], hint_text="Entry ID Lokasi", font_size='16sp')
        self.in_id_msk = TextInput(text=s['id_msk'], hint_text="Entry ID Masak", font_size='16sp')
        self.in_id_cat = TextInput(text=s['id_cat'], hint_text="Entry ID Catatan", font_size='16sp')
        btn = Button(text="SIMPAN KONFIGURASI", background_color=(0, 1, 0, 1), size_hint_y=None, height=dp(60), font_size='22sp', bold=True)
        btn.bind(on_press=self.save_cfg)
        for w in [self.in_url, self.in_id_loc, self.in_id_msk, self.in_id_cat, btn]: content.add_widget(w)
        self.ad_pop = Popup(title="Konfigurasi Form", content=content, size_hint=(0.95, 0.9)); self.ad_pop.open()

    def save_cfg(self, instance):
        self.config_store.put('settings', url=self.in_url.text, id_loc=self.in_id_loc.text, 
                              id_msk=self.in_id_msk.text, id_tot='', id_mkl='', id_mda='', id_cat=self.in_id_cat.text)
        self.ad_pop.dismiss(); self.status_bar.text = "Konfigurasi Disimpan!"

if __name__ == '__main__':
    PalmGradeApp().run()
