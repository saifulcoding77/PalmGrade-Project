import cv2
import numpy as np
import os
import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class PalmScanner(BoxLayout):
    def __init__(self, **kwargs):
        super(PalmScanner, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Folder untuk simpan imej bukti
        if not os.path.exists('reports'): 
            os.makedirs('reports')
            
        self.capture = cv2.VideoCapture(0)
        self.img_output = Image()
        self.add_widget(self.img_output)

        # PARAMETER KAWALAN (DEFAULT)
        self.gamma_val = 1.5 
        self.min_sockets_req = 5    
        self.orange_sensitivity = 0.35 
        self.is_admin = False
        self.counts = {"Total": 0, "Masak": 0, "Overripe": 0, "Mengkal": 0, "Muda": 0}
        self.current_frame = None
        
        Clock.schedule_interval(self.update, 1.0 / 20)

    def apply_auto_tune(self, frame):
        """Melaraskan kecerahan secara automatik (AI Auto-Tune)"""
        avg = np.mean(frame)
        if avg < 100: self.gamma_val = min(2.8, self.gamma_val + 0.02)
        elif avg > 150: self.gamma_val = max(0.7, self.gamma_val - 0.02)
        
        inv_gamma = 1.0 / self.gamma_val
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(frame, table)

    def detect_sockets(self, roi_gray):
        """Mengira soket kosong (biji relai)"""
        _, thresh = cv2.threshold(roi_gray, 45, 255, cv2.THRESH_BINARY_INV)
        cnts, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return sum(1 for c in cnts if 50 < cv2.contourArea(c) < 600)

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret: return
        
        proc_frame = self.apply_auto_tune(frame)
        hsv = cv2.cvtColor(proc_frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(proc_frame, cv2.COLOR_BGR2GRAY)
        
        # Range warna oren/merah sawit masak
        mask_orange = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([22, 255, 255]))
        mask_all = cv2.inRange(hsv, np.array([0, 10, 10]), np.array([180, 255, 255]))
        
        cnts, _ = cv2.findContours(mask_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        t_counts = {"Total": 0, "Masak": 0, "Overripe": 0, "Mengkal": 0, "Muda": 0}

        for c in cnts:
            if cv2.contourArea(c) > 4000:
                t_counts["Total"] += 1
                x,y,w,h = cv2.boundingRect(c)
                density = cv2.countNonZero(mask_orange[y:y+h, x:x+w]) / (w*h+1)
                skt = self.detect_sockets(gray[y:y+h, x:x+w])

                # LOGIK GREDING
                if density >= self.orange_sensitivity and skt >= self.min_sockets_req:
                    label, color = f"MASAK ({skt} Skt)", (0,255,0)
                    t_counts["Masak"] += 1
                elif density > 0.65 or skt > 15:
                    label, color = "OVERRIPE", (0,255,255)
                    t_counts["Overripe"] += 1
                elif 0.10 <= density < self.orange_sensitivity:
                    label, color = "MENGKAL", (0,165,255)
                    t_counts["Mengkal"] += 1
                else:
                    label, color = "MUDA", (0,0,255)
                    t_counts["Muda"] += 1

                cv2.rectangle(proc_frame, (x,y), (x+w,y+h), color, 3)
                cv2.putText(proc_frame, label, (x, y-10), 0, 0.7, color, 2)

        self.counts = t_counts
        self.current_frame = proc_frame
        self.draw_hud(proc_frame)
        self.img_output.texture = self.convert_to_texture(proc_frame)

    def draw_hud(self, frame):
        """Paparan Maklumat Utama (HUD)"""
        cv2.rectangle(frame, (10, 10), (550, 160), (0,0,0), -1)
        status = "ADMIN (UNLOCKED)" if self.is_admin else "OPERATOR (LOCKED)"
        cv2.putText(frame, status, (20, 40), 0, 0.7, (255,255,0), 2)
        cv2.putText(frame, f"SENS: {self.orange_sensitivity:.2f} | SKT: {self.min_sockets_req} | GM: {self.gamma_val:.1f}", (20, 75), 0, 0.5, (200,200,200), 1)
        cv2.putText(frame, f"TOTAL: {self.counts['Total']} | MASAK: {self.counts['Masak']}", (20, 110), 0, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"MENGKAL: {self.counts['Mengkal']} | MUDA: {self.counts['Muda']}", (20, 145), 0, 0.6, (0,0,255), 2)

    def convert_to_texture(self, bgr):
        buf = cv2.flip(bgr, 0).tobytes()
        tex = Texture.create(size=(bgr.shape[1], bgr.shape[0]), colorfmt='bgr')
        tex.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return tex

class PalmGradeApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        self.scanner = PalmScanner()
        self.root.add_widget(self.scanner)
        
        # PANEL MAKLUMAT (LOKASI & CATATAN)
        input_panel = BoxLayout(size_hint_y=0.15, padding=5, spacing=5)
        self.txt_lokasi = TextInput(hint_text="Nama Lokasi / Blok", multiline=False)
        self.txt_catatan = TextInput(hint_text="Catatan (No. Plat / Pekerja)", multiline=False)
        input_panel.add_widget(self.txt_lokasi)
        input_panel.add_widget(self.txt_catatan)
        self.root.add_widget(input_panel)

        # PANEL OPERATOR (SIMPAN)
        op_layout = BoxLayout(size_hint_y=0.15, padding=10, spacing=10)
        btn_save = Button(text="SIMPAN REKOD", background_color=(0,0.6,0,1), bold=True)
        btn_save.bind(on_press=self.quick_save)
        
        btn_snap = Button(text="SIMPAN BUKTI", background_color=(1,0.5,0,1))
        btn_snap.bind(on_press=self.save_with_img)
        
        btn_admin = Button(text="🔑 ADMIN", size_hint_x=0.3)
        btn_admin.bind(on_press=self.auth_popup)
        
        op_layout.add_widget(btn_save); op_layout.add_widget(btn_snap); op_layout.add_widget(btn_admin)
        self.root.add_widget(op_layout)

        # PANEL ADMIN (TERSEMBUYI)
        self.admin_layout = BoxLayout(size_hint_y=0.12, padding=5, spacing=5, opacity=0, disabled=True)
        
        btn_s_up = Button(text="+1 Soket"); btn_s_up.bind(on_press=lambda x: setattr(self.scanner, 'min_sockets_req', self.scanner.min_sockets_req + 1))
        btn_s_dw = Button(text="-1 Soket"); btn_s_dw.bind(on_press=lambda x: setattr(self.scanner, 'min_sockets_req', max(1, self.scanner.min_sockets_req - 1)))
        
        btn_sens_up = Button(text="+ Sens Warna", background_color=(0,0.7,0.7,1))
        btn_sens_up.bind(on_press=lambda x: setattr(self.scanner, 'orange_sensitivity', min(0.9, self.scanner.orange_sensitivity + 0.05)))
        
        btn_sens_dw = Button(text="- Sens Warna", background_color=(0,0.7,0.7,1))
        btn_sens_dw.bind(on_press=lambda x: setattr(self.scanner, 'orange_sensitivity', max(0.1, self.scanner.orange_sensitivity - 0.05)))
        
        btn_res = Button(text="RESET", background_color=(1,0,0,1))
        btn_res.bind(on_press=self.reset_data)
        
        self.admin_layout.add_widget(btn_s_up); self.admin_layout.add_widget(btn_s_dw)
        self.admin_layout.add_widget(btn_sens_up); self.admin_layout.add_widget(btn_sens_dw)
        self.admin_layout.add_widget(btn_res)
        self.root.add_widget(self.admin_layout)
        
        return self.root

    def auth_popup(self, instance):
        if not self.scanner.is_admin:
            box = BoxLayout(orientation='vertical', padding=10, spacing=10)
            self.pw = TextInput(password=True, multiline=False, hint_text="Password")
            btn = Button(text="Login")
            btn.bind(on_press=self.verify)
            box.add_widget(self.pw); box.add_widget(btn)
            self.pop = Popup(title="Admin Access", content=box, size_hint=(0.6, 0.4)); self.pop.open()
        else:
            self.scanner.is_admin = False; self.admin_layout.opacity = 0; self.admin_layout.disabled = True; instance.text = "🔑 ADMIN"

    def verify(self, instance):
        if self.pw.text == "MPOB2024":
            self.scanner.is_admin = True; self.admin_layout.opacity = 1; self.admin_layout.disabled = False; self.pop.dismiss()
        else: self.pw.hint_text = "SALAH!"

    def quick_save(self, instance):
        loc = self.txt_lokasi.text if self.txt_lokasi.text else "N/A"
        cat = self.txt_catatan.text if self.txt_catatan.text else "N/A"
        csv_file = "rekod_harian_sawit.csv"
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Masa", "Lokasi", "Catatan", "Total", "Masak", "Overripe", "Mengkal", "Muda", "Status_Imej"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), loc, cat,
                self.scanner.counts['Total'], self.scanner.counts['Masak'],
                self.scanner.counts['Overripe'], self.scanner.counts['Mengkal'],
                self.scanner.counts['Muda'], "DATA_ONLY"
            ])
        
        self.txt_catatan.text = ""
        instance.text = "TERSIMPAN! ✅"; Clock.schedule_once(lambda dt: setattr(instance, 'text', "SIMPAN REKOD"), 1.5)

    def save_with_img(self, instance):
        loc = self.txt_lokasi.text if self.txt_lokasi.text else "N/A"
        cat = self.txt_catatan.text if self.txt_catatan.text else "N/A"
        ts = datetime.now().strftime('%H%M%S')
        fn = f"reports/Bukti_{ts}.jpg"
        
        if self.scanner.current_frame is not None:
            cv2.imwrite(fn, self.scanner.current_frame)
            
        with open("rekod_harian_sawit.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), loc, cat,
                self.scanner.counts['Total'], self.scanner.counts['Masak'],
                self.scanner.counts['Overripe'], self.scanner.counts['Mengkal'],
                self.scanner.counts['Muda'], fn
            ])
        instance.text = "IMEJ OK! 📸"; Clock.schedule_once(lambda dt: setattr(instance, 'text', "SIMPAN BUKTI"), 1.5)

    def reset_data(self, instance):
        self.scanner.counts = {k:0 for k in self.scanner.counts}

if __name__ == '__main__':
    PalmGradeApp().run()