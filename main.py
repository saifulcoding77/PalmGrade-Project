import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from android.permissions import request_permissions, Permission

class PalmGradeApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        
        # 1. Tambah Label Status
        self.status_label = Label(text="Memulakan Kamera...", size_hint_y=0.1)
        self.root.add_widget(self.status_label)
        
        # 2. Cuba buka Kamera dengan Error Handling
        try:
            self.camera = Camera(play=True, resolution=(640, 480), index=0)
            self.root.add_widget(self.camera)
            self.status_label.text = "Kamera Aktif - Sedia untuk Analisis"
        except Exception as e:
            self.status_label.text = f"Ralat Kamera: {str(e)}"
            
        return self.root

    def on_start(self):
        if platform == 'android':
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])
            # Beri masa 1 saat untuk sistem proses izin sebelum buka kamera
            Clock.schedule_once(self.start_camera, 1)

    def start_camera(self, dt):
        if hasattr(self, 'camera'):
            self.camera.play = True

if __name__ == '__main__':
    PalmGradeApp().run()
