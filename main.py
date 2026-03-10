from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.clock import Clock

class PalmGradeLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Jangan letak Camera(play=True) terus di sini.
        # Kita tunggu 1 saat selepas aplikasi dibuka.
        Clock.schedule_once(self.start_camera, 1)

    def start_camera(self, dt):
        try:
            self.camera = Camera(play=True, resolution=(640, 480))
            self.ids.camera_container.add_widget(self.camera)
            Clock.schedule_interval(self.analisis_buah, 0.5)
        except Exception as e:
            print(f"Ralat Kamera: {e}")

    def analisis_buah(self, dt):
        # Logik pengesanan anda di sini
        pass

    def simpan_data(self):
        print("Data tersimpan!")

class PalmGradeApp(App):
    def build(self):
        return PalmGradeLayout()

if __name__ == '__main__':
    PalmGradeApp().run()
