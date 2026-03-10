from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.clock import Clock

class PalmGradeLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Tunggu 1 saat supaya UI siap dibina sebelum buka kamera
        Clock.schedule_once(self.start_camera, 1)

    def start_camera(self, dt):
        try:
            # Gunakan resolusi -1 untuk kestabilan Android
            self.camera = Camera(play=True, resolution=(-1, -1))
            self.ids.camera_container.add_widget(self.camera)
        except Exception as e:
            self.ids.status_label.text = f"Error: {str(e)}"

    def simpan_data(self):
        self.ids.status_label.text = "DATA DISIMPAN!"

class PalmGradeApp(App):
    def build(self):
        return PalmGradeLayout()

if __name__ == '__main__':
    PalmGradeApp().run()
