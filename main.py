from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock

class PalmGradeApp(App):
    def build(self):
        # Layout utama
        self.layout = BoxLayout(orientation='vertical')
        
        # 1. Label Keputusan (Diperkecilkan sedikit supaya stabil)
        self.result_label = Label(
            text="HALAKAN KE BUAH SAWIT",
            size_hint_y=0.2,
            font_size='24sp',
            bold=True
        )
        self.layout.add_widget(self.result_label)
        
        # 2. Kamera (Versi Paling Ringan)
        # Kita tidak guna Rotate atau PushMatrix di sini untuk elak crash
        self.cam = Camera(
            play=True, 
            resolution=(640, 480), 
            index=0, 
            allow_stretch=True, # Kita besarkan tapi tanpa pusingan grafik
            size_hint=(1, 0.7)   # Beri 70% ruang skrin untuk kamera
        )
        self.layout.add_widget(self.cam)
        
        # 3. Label Sensor
        self.sensor_label = Label(text="Menganalisis...", size_hint_y=0.1)
        self.layout.add_widget(self.sensor_label)
        
        Clock.schedule_interval(self.analyze_palm, 0.5)
        return self.layout

    def analyze_palm(self, dt):
        if not self.cam.texture:
            return
        try:
            tex = self.cam.texture
            w, h = tex.width, tex.height
            # Kita tukar koordinat analisis (X dan Y terbalik) 
            # kerana sensor senget 90 darjah, jadi kita analisa titik yang betul
            region = tex.get_region(int(w/2)-10, int(h/2)-10, 20, 20)
            pixels = region.pixels
            
            r_vals = [pixels[i] for i in range(0, len(pixels), 4)]
            g_vals = [pixels[i+1] for i in range(0, len(pixels), 4)]
            
            avg_r = sum(r_vals) / len(r_vals)
            avg_g = sum(g_vals) / len(g_vals)
            
            # Logik Greding
            if avg_r > (avg_g * 1.35) and avg_r > 90:
                self.result_label.text = "GRED: MASAK (LULUS)"
                self.result_label.color = (0.2, 1, 0.2, 1)
            elif avg_r > (avg_g * 1.1) and avg_r > 70:
                self.result_label.text = "GRED: MENGKAL"
                self.result_label.color = (1, 1, 0, 1)
            else:
                self.result_label.text = "GRED: MUDA / HITAM"
                self.result_label.color = (1, 0.2, 0.2, 1)
                
            self.sensor_label.text = f"Sensor R: {int(avg_r)} | G: {int(avg_g)}"
        except:
            pass

if __name__ == '__main__':
    PalmGradeApp().run()
