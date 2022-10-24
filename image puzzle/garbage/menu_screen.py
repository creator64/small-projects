from tkinter import *
from tkinter import ttk
from game_screen import GameScreen


class MenuScreen:
    def __init__(self, canvas):
        self.canvas = canvas
        MainLabel = Label(canvas, text="IMAGEPUZZLER", font=("Courier", 25)); MainLabel.pack()
        DifficultyLabel = Label(canvas, text="choose diffilculty", font=("Courier", 15)); DifficultyLabel.pack()
        self.combo = ttk.Combobox(canvas, font=("Courier", 15), values=["easy","medium","hard","insane","impossible"], state="readonly"); self.combo.pack(); self.combo.set("medium")
        PlayButton = Button(canvas, text="play", font=("Courier", 25), command=self.play); PlayButton.pack(pady=20)

    def play(self):
        difficulty = self.combo.get()
        self.canvas.show_screen(GameScreen, args=(difficulty,))
