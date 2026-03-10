from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.properties import ObjectProperty

class PalmGradeLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Tambah kamera secara dinamik supaya Rotate berfungsi tepat
        self.camera = Camera(play=True, resolution=(640, 480))
        self.ids.camera_container.add_widget(self.camera)
        Clock.schedule_interval(self.analisis_buah, 0.5)

    def analisis_buah(self, dt):
        # Simulasi AI Pengesanan
        # Sila hubungkan dengan model .tflite anda di sini
        status = "MASAK"  # Contoh hasil pengesanan
        
        label = self.ids.status_label
        button = self.ids.btn_sah
        
        if status == "MASAK":
            label.text = "[color=00FF00]BUAH MASAK[/color]"
            button.disabled = False
            button.background_color = (0, 1, 0, 1)
        elif status == "MENGKAL":
            label.text = "[color=FFFF00]MENGKAL (JANGAN TUAI)[/color]"
            button.disabled = True
            button.background_color = (0.5, 0.5, 0.5, 1)
        else:
            label.text = "MENCARI..."
            button.disabled = True

    def simpan_data(self):
        print("Data tersimpan dalam Modul Kuih Lepat!")

    def reset_kiraan(self):
        print("Kiraan telah dikosongkan.")

class PalmGradeApp(App):
    def build(self):
        return PalmGradeLayout()

if __name__ == '__main__':
    PalmGradeApp().run()
