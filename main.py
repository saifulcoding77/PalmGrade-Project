from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock

class PalmGradeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # 1. Label Keputusan
        self.result_label = Label(
            text="PalmGrade AI (Safe Mode)\nMenunggu Analisis...",
            size_hint_y=0.2,
            font_size='20sp',
            halign='center'
        )
        self.layout.add_widget(self.result_label)
        
        # 2. Kamera Kivy Asas (Sangat Stabil)
        self.cam = Camera(play=True, resolution=(640, 480), index=0)
        self.layout.add_widget(self.cam)
        
        # Analisis warna setiap 1 saat
        Clock.schedule_interval(self.analyze_color, 1.0)
        
        return self.layout

    def analyze_color(self, dt):
        if not self.cam.texture:
            return

        try:
            # Ambil warna dari satu titik di tengah-tengah skrin (Center Pixel)
            # Ini tidak membebankan memori seperti OpenCV
            texture = self.cam.texture
            center_x, center_y = int(texture.width / 2), int(texture.height / 2)
            pixel_data = texture.get_region(center_x, center_y, 1, 1).pixels
            
            # Ambil nilai RGB (Red, Green, Blue)
            r, g, b, a = pixel_data[0], pixel_data[1], pixel_data[2], pixel_data[3]
            
            # --- LOGIK GRED SAWIT BERASASKAN RGB ---
            # Jika merah/oren tinggi, ia adalah buah masak
            if r > 150 and g < 100:
                self.result_label.text = f"GRED: MASAK\n(R:{r} G:{g} B:{b})"
                self.result_label.color = (0, 1, 0, 1) # Hijau
            elif r > 100 and g > 80:
                self.result_label.text = f"GRED: MENGKAL\n(R:{r} G:{g} B:{b})"
                self.result_label.color = (1, 1, 0, 1) # Kuning
            else:
                self.result_label.text = f"GRED: MUDA / HITAM\n(R:{r} G:{g} B:{b})"
                self.result_label.color = (1, 0, 0, 1) # Merah
                
        except Exception as e:
            pass

if __name__ == '__main__':
    PalmGradeApp().run()
