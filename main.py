import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform

class PalmGradeApp(App):
    def build(self):
        # 1. Inisialisasi Simpanan (Database Kecil)
        self.store = JsonStore('admin_config.json')
        if not self.store.exists('settings'):
            # Nilai default jika belum pernah diset
            self.store.put('settings', url='', id_loc='', id_tot='', id_msk='', id_mkl='', id_mda='', id_cat='')
        
        self.count = {"Masak": 0, "Mengkal": 0, "Muda": 0, "Total": 0}
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # 2. UI Utama
        self.cam = Camera(play=True, resolution=(640, 480), allow_stretch=True, size_hint=(1, 0.4))
        self.layout.add_widget(self.cam)
        
        self.score_board = Label(text="Total: 0 | Msk: 0 | Mkl: 0 | Mda: 0", size_hint_y=0.1, bold=True)
        self.layout.add_widget(self.score_board)

        self.txt_lokasi = TextInput(text='Lokasi', multiline=False, size_hint_y=0.08)
        self.txt_catatan = TextInput(text='Catatan', multiline=False, size_hint_y=0.08)
        self.layout.add_widget(self.txt_lokasi)
        self.layout.add_widget(self.txt_catatan)
        
        # 3. Butang Operasi
        btn_action = BoxLayout(size_hint_y=0.12, spacing=5)
        btn_msk = Button(text="MASAK+1", background_color=(0.2, 0.8, 0.2, 1))
        btn_msk.bind(on_press=lambda x: self.tambah("Masak"))
        btn_action.add_widget(btn_msk)
        self.layout.add_widget(btn_action)
        
        # 4. Butang Hantar & Admin
        footer = BoxLayout(size_hint_y=0.12, spacing=10)
        btn_cloud = Button(text="HANTAR CLOUD", background_color=(0.1, 0.5, 0.8, 1), bold=True)
        btn_cloud.bind(on_press=self.hantar_ke_cloud)
        
        btn_admin = Button(text="ADMIN", size_hint_x=0.3, background_color=(0.4, 0.4, 0.4, 1))
        btn_admin.bind(on_press=self.show_password_popup)
        
        footer.add_widget(btn_cloud)
        footer.add_widget(btn_admin)
        self.layout.add_widget(footer)

        self.status_label = Label(text="Status: Sedia", size_hint_y=0.05, font_size='12sp')
        self.layout.add_widget(self.status_label)
        
        return self.layout

    # --- FUNGSI ADMIN & PASSWORD ---
    def show_password_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.pwd_input = TextInput(password=True, multiline=False, hint_text="Masukkan Password Admin")
        btn = Button(text="MASUK", size_hint_y=0.4)
        btn.bind(on_press=self.check_password)
        content.add_widget(self.pwd_input)
        content.add_widget(btn)
        self.popup = Popup(title="Security Check", content=content, size_hint=(0.8, 0.4))
        self.popup.open()

    def check_password(self, instance):
        if self.pwd_input.text == "admin123": # <--- GANTI PASSWORD ANDA DI SINI
            self.popup.dismiss()
            self.open_admin_panel()
        else:
            self.status_label.text = "Password Salah!"

    def open_admin_panel(self):
        s = self.store.get('settings')
        content = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        self.in_url = TextInput(text=s['url'], hint_text="URL Form Response")
        self.in_id_loc = TextInput(text=s['id_loc'], hint_text="ID Lokasi")
        self.in_id_msk = TextInput(text=s['id_msk'], hint_text="ID Masak")
        self.in_id_tot = TextInput(text=s['id_tot'], hint_text="ID Total")
        
        btn_save = Button(text="SIMPAN KONFIGURASI", background_color=(0, 1, 0, 1))
        btn_save.bind(on_press=self.save_config)
        
        for widget in [self.in_url, self.in_id_loc, self.in_id_msk, self.in_id_tot, btn_save]:
            content.add_widget(widget)
            
        self.admin_popup = Popup(title="Admin Panel", content=content, size_hint=(0.9, 0.8))
        self.admin_popup.open()

    def save_config(self, instance):
        self.store.put('settings', 
            url=self.in_url.text, id_loc=self.in_id_loc.text, 
            id_msk=self.in_id_msk.text, id_tot=self.in_id_tot.text,
            id_mkl='', id_mda='', id_cat='')
        self.admin_popup.dismiss()
        self.status_label.text = "Konfigurasi Dikemaskini!"

    def hantar_ke_cloud(self, instance):
        s = self.store.get('settings')
        if not s['url']:
            self.status_label.text = "Ralat: Set URL di Admin!"
            return

        params = {
            s['id_loc']: self.txt_lokasi.text,
            s['id_msk']: str(self.count['Masak']),
            s['id_tot']: str(self.count['Total']),
        }
        UrlRequest(s['url'], req_body=params, on_success=lambda r, v: self.on_success())

    def on_success(self):
        self.status_label.text = "Berjaya dihantar!"
        for k in self.count: self.count[k] = 0

    def tambah(self, gred):
        self.count[gred] += 1
        self.count["Total"] += 1
        self.score_board.text = f"Total: {self.count['Total']} | Msk: {self.count['Masak']}"

if __name__ == '__main__':
    PalmGradeApp().run()
