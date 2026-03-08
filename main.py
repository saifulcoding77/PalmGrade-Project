import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture

class PalmGradeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # 1. Label Keputusan Gred
        self.result_label = Label(
            text="Sila Halakan Kamera ke Buah Sawit",
            size_hint_y=0.2,
            font_size='20sp',
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.result_label)
        
        # 2. Kamera (Tetapan Stabil Vivo)
        self.cam = Camera(play=True, resolution=(640, 480), index=0)
        self.layout.add_widget(self.cam)
        
        # Mulakan analisis automatik setiap 2 saat
        Clock.schedule_interval(self.analyze_frame, 2.0)
        
        return self.layout

    def analyze_frame(self, dt):
        if not self.cam.play:
            return

        try:
            # Ambil data imej dari kamera Kivy
            texture = self.cam.texture
            size = texture.size
            pixels = texture.pixels
            
            # Tukar ke format OpenCV (numpy array)
            frame = np.frombuffer(pixels, dtype=np.uint8)
            frame = frame.reshape(size[1], size[0], 4)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            
            # --- LOGIK GRED SAWIT (Warna HSV) ---
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Julat warna oren/merah untuk buah masak
            lower_orange = np.array([5, 100, 100])
            upper_orange = np.array([25, 255, 255])
            
            mask = cv2.inRange(hsv, lower_orange, upper_orange)
            orange_pixels = cv2.countNonZero(mask)
            
            # Tentukan Gred berdasarkan jumlah pixel oren
            if orange_pixels > 5000:
                self.result_label.text = "GRED: MASAK (READY)"
                self.result_label.color = (0, 1, 0, 1) # Hijau
            elif orange_pixels > 1000:
                self.result_label.text = "GRED: MENGKAL"
                self.result_label.color = (1, 1, 0, 1) # Kuning
            else:
                self.result_label.text = "GRED: MUDA / HITAM"
                self.result_label.color = (1, 0, 0, 1) # Merah
                
        except Exception as e:
            # Jika ralat, jangan tutup aplikasi, cuma tunjuk ralat di label
            self.result_label.text = "Menunggu Data Visual..."

if __name__ == '__main__':
    PalmGradeApp().run()
