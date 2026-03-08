from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.clock import Clock

# Hanya import modul Android jika dijalankan pada telefon
if platform == 'android':
    from android.permissions import request_permissions, Permission

class TestApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Label Status
        self.label = Label(
            text="PalmGrade AI: Ujian Kestabilan\nStatus: Menunggu Izin Kamera",
            halign='center'
        )
        self.layout.add_widget(self.label)
        
        # Butang Ujian
        self.btn = Button(text="KLIK JIKA NAMPAK", size_hint=(1, 0.2))
        self.btn.bind(on_press=self.button_pressed)
        self.layout.add_widget(self.btn)
        
        return self.layout

    def on_start(self):
        # Minta izin kamera sebaik aplikasi dibuka
        if platform == 'android':
            request_permissions([Permission.CAMERA])
            Clock.schedule_once(self.check_permissions, 2)

    def check_permissions(self, dt):
        self.label.text = "Sistem OK!\nSila benarkan akses kamera jika muncul."

    def button_pressed(self, instance):
        self.label.text = "Butang Berfungsi!\nSistem Kivy anda stabil."

if __name__ == '__main__':
    TestApp().run()
