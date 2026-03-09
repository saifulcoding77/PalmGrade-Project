import time
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform

class PalmGradeApp(App):
    def build(self):
        self.count = {"Masak": 0, "Mengkal": 0, "Muda": 0, "Total": 0}
        self.is_waiting_for_relai = False
        
        # Folder simpanan fail
        self.log_file = "laporan_sawit.csv"
        self.create_csv_header()

        # Layout Utama
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # 1. Kamera (Saiz dikecilkan sedikit untuk ruang input)
        self.cam = Camera(play=True, resolution=(640, 480), allow_stretch=True, size_hint=(1, 0.35))
        self.layout.add_widget(self.cam)
        
        # 2. Papan Markah
        self.score_board = Label(
            text="Total: 0 | Masak: 0 | Mengkal: 0 | Muda: 0",
            size_hint_y=0.08, font_size='16sp', color=(0, 1, 1, 1), bold=True
        )
        self.layout.add_widget(self.score_board)

        # 3. Input Manual (Lokasi & Catatan)
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.2, spacing=5)
        self.txt_lokasi = TextInput(text='Lokasi Ladang', multiline=False, font_size='14sp')
        self.txt_catatan = TextInput(text='Catatan (cth: Blok A)', multiline=False, font_size='14sp')
        input_layout.add_widget(self.txt_lokasi)
        input_layout.add_widget(self.txt_catatan)
        self.layout.add_widget(input_layout)
        
        # 4. Butang Aksi Utama
        self.btn_relai = Button(
            text="SAHKAN RELAI (MASAK +1)", 
            size_hint_y=0.12, background_color=(0.2, 0.8, 0.2, 1), bold=True
        )
        self.btn_relai.bind(on_press=self.confirm_masak)
        self.layout.add_widget(self.btn_relai)

        # 5. Butang Gred Lain (Manual Count)
        gred_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        btn_mengkal = Button(text="MENGKAL +1", background_color=(0.8, 0.8, 0.2, 1))
        btn_mengkal.bind(on_press=lambda x: self.tambah_manual("Mengkal"))
        btn_muda = Button(text="MUDA +1", background_color=(0.8, 0.2, 0.2, 1))
        btn_muda.bind(on_press=lambda x: self.tambah_manual("Muda"))
        gred_layout.add_widget(btn_mengkal)
        gred_layout.add_widget(btn_muda)
        self.layout.add_widget(gred_layout)
        
        # 6. Butang Simpan & Reset
        save_layout = BoxLayout(size_hint_y=0.12, spacing=10)
        btn_save = Button(text="SIMPAN KE EXCEL", background_color=(0.1, 0.5, 0.8, 1), bold=True)
        btn_save.bind(on_press=self.save_to_csv)
        btn_reset = Button(text="RESET", background_color=(0.4, 0.4, 0.4, 1))
        btn_reset.bind(on_press=self.reset_count)
        save_layout.add_widget(btn_save)
        save_layout.add_widget(btn_reset)
        self.layout.add_widget(save_layout)

        self.status_label = Label(text="Sedia untuk operasi", size_hint_y=0.05, font_size='12sp')
        self.layout.add_widget(self.status_label)
        
        return self.layout

    def create_csv_header(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("Tarikh,Masa,Lokasi,Total,Masak,Mengkal,Muda,Catatan\n")

    def tambah_manual(self, gred):
        self.count[gred] += 1
        self.count["Total"] += 1
        self.kemaskini_papan()

    def confirm_masak(self, instance):
        self.count["Masak"] += 1
        self.count["Total"] += 1
        self.kemaskini_papan()

    def save_to_csv(self, instance):
        tarikh = time.strftime("%d/%m/%Y")
        masa = time.strftime("%H:%M:%S")
        lokasi = self.txt_lokasi.text.replace(",", ";") # Elak ralat format CSV
        catatan = self.txt_catatan.text.replace(",", ";")
        
        baris_data = f"{tarikh},{masa},{lokasi},{self.count['Total']},{self.count['Masak']},{self.count['Mengkal']},{self.count['Muda']},{catatan}\n"
        
        try:
            with open(self.log_file, "a") as f:
                f.write(baris_data)
            self.status_label.text = f"Data disimpan ke {self.log_file}"
        except Exception as e:
            self.status_label.text = "Ralat simpan fail!"

    def kemaskini_papan(self):
        self.score_board.text = (f"Total: {self.count['Total']} | Masak: {self.count['Masak']} | "
                                 f"Mengkal: {self.count['Mengkal']} | Muda: {self.count['Muda']}")

    def reset_count(self, instance):
        for key in self.count: self.count[key] = 0
        self.kemaskini_papan()
        self.status_label.text = "Kiraan telah direset"

if __name__ == '__main__':
    PalmGradeApp().run()
