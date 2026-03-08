from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock
from kivy.graphics.rotate import Rotate
from kivy.graphics.context_instructions import PushMatrix, PopMatrix

if platform == 'android':
    from android.permissions import request_permissions, Permission

class PalmGradeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Label Status yang lebih kemas
        self.status = Label(text="PalmGrade AI - Sedia", size_hint_y=0.1)
        self.layout.add_widget(self.status)
        
        # Tetapan Kamera untuk skrin penuh dan pusingan
        self.cam = Camera(
            play=False, 
            resolution=(1280, 720), # Resolusi lebih tinggi untuk Vivo
            index=0,
            allow_stretch=True,     # Supaya gambar besar
            keep_ratio=True         # Kekalkan nisbah aspek
        )
        
        # Logik untuk memusingkan kamera yang senget
        with self.cam.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=-90, origin=self.cam.center) # Pusing 90 darjah ke kanan
        with self.cam.canvas.after:
            PopMatrix()
            
        # Kemaskini pusat pusingan jika saiz skrin berubah
        self.cam.bind(pos=self.update_rotate, size=self.update_rotate)
        
        self.layout.add_widget(self.cam)
        return self.layout

    def update_rotate(self, instance, value):
        self.rot.origin = self.cam.center

    def on_start(self):
        if platform == 'android':
            request_permissions([Permission.CAMERA], self.check_p)
        else:
            self.cam.play = True

    def check_p(self, permissions, results):
        if all(results):
            Clock.schedule_once(self.start_cam, 1)

    def start_cam(self, dt):
        self.cam.play = True
        self.status.text = "Analisis Visual Aktif"

if __name__ == '__main__':
    PalmGradeApp().run()
