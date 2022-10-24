from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from menu_screen import Menu_Screen
from kivy.lang.builder import Builder

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        return sm


app = MainApp()
Builder.load_file("kvfiles/menu_screen.kv"); Builder.load_file("kvfiles/game_screen.kv")
sm = ScreenManager()
sm.add_widget(Menu_Screen(name="menu"))

app.run()
