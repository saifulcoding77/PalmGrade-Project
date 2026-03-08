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
        self.layout = BoxLayout(orientation='vertical')
        self.status = Label(text="Memulakan Kamera Vivo...", size_hint_y=0.1)
        self.layout.add_widget(self.status)
        
        # Gunakan resolusi standard Android
        self.cam = Camera(play=False, resolution=(640, 480), index=0)
        self.layout.add_widget(self.cam)
        
        return self.layout

    def on_start(self):
        if platform == 'android':
            request_permissions([Permission.CAMERA], self.check_p)
        else:
            self.cam.play = True

    def check_p(self, permissions, results):
        if all(results):
            self.status.text = "Kamera Aktif"
            # Beri sedikit ruang sebelum 'play'
            Clock.schedule_once(self.start_cam, 1)
        else:
            self.status.text = "Izin Ditolak"

    def start_cam(self, dt):
        self.cam.play = True

if __name__ == '__main__':
    PalmGradeApp().run()
