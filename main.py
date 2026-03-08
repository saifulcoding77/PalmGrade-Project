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
        self.status_label = Label(text="Sistem PalmGrade Dimulakan...", size_hint_y=0.1)
        self.root.add_widget(self.status_label)
        return self.root

    def on_start(self):
        if platform == 'android':
            # Minta izin secara rasmi
            request_permissions([Permission.CAMERA], self.check_permissions)
        else:
            self.start_camera()

    def check_permissions(self, permissions, results):
        # Jika semua izin diberikan (results adalah list of booleans)
        if all(results):
            self.status_label.text = "Izin Diterima. Menghidupkan Kamera..."
            # Tunggu 1.5 saat supaya sistem Android sedia
            Clock.schedule_once(self.start_camera, 1.5)
        else:
            self.status_label.text = "Izin Kamera Ditolak!"

    def start_camera(self, dt=0):
        try:
            # Resolusi rendah (320x240) untuk ujian kestabilan pada Vivo
            self.camera = Camera(play=True, resolution=(320, 240), index=0)
            self.root.add_widget(self.camera)
            self.status_label.text = "Kamera Aktif (Vivo V21)"
        except Exception as e:
            self.status_label.text = f"Ralat: {str(e)}"

if __name__ == '__main__':
    PalmGradeApp().run()
