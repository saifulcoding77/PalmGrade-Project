from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.rotate import Rotate
from kivy.graphics.context_instructions import PushMatrix, PopMatrix

class PalmGradeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # 1. Header Keputusan
        self.result_label = Label(
            text="PALMGRADE AI: READY",
            size_hint_y=0.15,
            font_size='28sp',
            bold=True
        )
        self.layout.add_widget(self.result_label)
        
        # 2. Kamera dengan Pusingan Grafik (Fix 90 Degree)
        self.cam = Camera(
            play=True, 
            resolution=(640, 480), 
            index=0, 
            allow_stretch=True, 
            keep_ratio=False
        )
        
        # Logik memusingkan paparan kamera ke Portrait
        with self.cam.canvas.before:
            PushMatrix()
            # Kita pusing -90 darjah (atau 270) untuk betulkan orientasi Vivo
            self.rot = Rotate(angle=-90, origin=self.cam.center)
        with self.cam.canvas.after:
            PopMatrix()

        # Pastikan pusat pusingan sentiasa di tengah walaupun skrin berubah saiz
        self.cam.bind(pos=self.update_rotate, size=self.update_rotate)
        
        self.layout.add_widget(self.cam)
        
        # 3. Footer Sensor
        self.sensor_label = Label(text="R: 0 | G: 0", size_hint_y=0.1)
        self.layout.add_widget(self.sensor_label)
        
        Clock.schedule_interval(self.analyze_palm, 0.5)
        return self.layout

    def update_rotate(self, instance, value):
        self.rot.origin = self.cam.center

    def analyze_palm(self, dt):
        if not self.cam.texture:
            return
        try:
            tex = self.cam.texture
            w, h = tex.width, tex.height
            # Ambil sampel kecil di tengah
            region = tex.get_region(int(w/2)-10, int(h/2)-10, 20, 20)
            pixels = region.pixels
            
            r_vals = [pixels[i] for i in range(0, len(pixels), 4)]
            g_vals = [pixels[i+1] for i in range(0, len(pixels), 4)]
            
            avg_r = sum(r_vals) / len(r_vals)
            avg_g = sum(g_vals) / len(g_vals)
            
            # Logik Auto-Tuning Ratio
            if avg_r > (avg_g * 1.35) and avg_r > 90:
                self.result_label.text = "GRED: MASAK (LULUS)"
                self.result_label.color = (0.2, 1, 0.2, 1)
            elif avg_r > (avg_g * 1.1) and avg_r > 70:
                self.result_label.text = "GRED: MENGKAL"
                self.result_label.color = (1, 1, 0, 1)
            else:
                self.result_label.text = "GRED: MUDA / HITAM"
                self.result_label.color = (1, 0.2, 0.2, 1)
                
            self.sensor_label.text = f"Analisis Visual - R: {int(avg_r)} | G: {int(avg_g)}"
        except:
            pass

if __name__ == '__main__':
    PalmGradeApp().run()
