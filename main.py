import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera

class PalmScanner(BoxLayout):
    def __init__(self, **kwargs):
        super(PalmScanner, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Gunakan Kivy Camera (Lebih stabil untuk Android)
        self.camera = Camera(play=True, resolution=(640, 480), index=0)
        self.add_widget(self.camera)

        # Output untuk hasil analisis
        self.img_result = Image()
        self.add_widget(self.img_result)

        self.gamma_val = 1.5 
        self.orange_sensitivity = 0.35 
        self.counts = {"Total": 0, "Masak": 0, "Muda": 0}
        
        # Jalankan analisis setiap 1 saat (supaya tidak berat)
        Clock.schedule_interval(self.analyze_frame, 1.0)

    def analyze_frame(self, dt):
        # Ambil imej dari Kivy Camera ke OpenCV
        if self.camera.texture:
            # Tukar texture ke array numpy (OpenCV format)
            frame_data = self.camera.texture.pixels
            w, h = self.camera.texture.size
            frame = np.frombuffer(frame_data, bytes).reshape(h, w, 4)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

            # LOGIK ANDA (Auto-Tune & Grading)
            avg = np.mean(frame)
            if avg < 100: self.gamma_val = min(2.8, self.gamma_val + 0.02)
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask_orange = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([22, 255, 255]))
            
            # (Analisis diringkaskan untuk kelajuan Android)
            cnts, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.counts["Total"] = len([c for c in cnts if cv2.contourArea(c) > 4000])
            
            # Paparkan hasil ke skrin
            buf = cv2.flip(frame, 0).tobytes()
            tex = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            tex.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img_result.texture = tex

class PalmGradeApp(App):
    def build(self):
        return PalmScanner()

if __name__ == '__main__':
    PalmGradeApp().run()
