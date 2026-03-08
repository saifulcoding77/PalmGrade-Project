from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class PalmGradeApp(App):
    def build(self):
        # Skrin hitam dengan teks putih sahaja
        layout = BoxLayout(orientation='vertical')
        label = Label(text="PalmGrade AI\nStatus: SISTEM STABIL", 
                      font_size='25sp', 
                      halign='center')
        layout.add_widget(label)
        return layout

if __name__ == '__main__':
    PalmGradeApp().run()
