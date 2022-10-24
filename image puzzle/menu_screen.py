from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from game_screen import Game_Screen

difficulties = ["easy","medium","hard","very hard","insane","impossible"]

class Menu_Screen(Screen):
    def __init__(self, **kwargs):
        self.difficulty = "medium"
        super().__init__(**kwargs)

        # creating menu for choosing difficulties
        menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda diff=i: self.menu_callback(diff)
            } for i in difficulties
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.difficulty_button,
            items = menu_items,
            width_mult = 4
        ) # end

    def menu_callback(self, diff):
        self.difficulty = diff
        self.menu.dismiss()
        self.ids.difficulty_label.text = "Difficulty: " + self.difficulty # updating the label showing what difficulty were currently on

    def play_game(self):
        gs = Game_Screen(self.difficulty, name="game_screen")
        self.manager.add_widget(gs)
        self.manager.current = "game_screen"
