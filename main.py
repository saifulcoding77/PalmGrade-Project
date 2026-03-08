from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

class PalmGradeApp(App):
    def build(self):
        # Kod paling asas: Hanya satu Label di tengah skrin
        return Label(text="Ujian Kestabilan Vivo V21\nSistem Android: " + str(platform))

if __name__ == '__main__':
    PalmGradeApp().run()
