from tkinter import *
from PIL import Image, ImageTk
from menu_screen import MenuScreen

class custom_canvas(Canvas):
    def __init__(self, *args, **kwargs):
        self.commands={}
        self.pics=[]
        super(custom_canvas, self).__init__(*args, **kwargs)
    
    def clear(self, exceptions=[]):
        for item in self.winfo_children():
            if item not in exceptions:
                item.destroy()
                try:
                    del self.commands[item]
                except:
                    pass

        for item in self.master.winfo_children():
            if item not in exceptions and item!=self:
                item.destroy()

    def show_screen(self, screen, args=(), kwargs={}):
        self.clear()
        s = screen(c, *args, **kwargs)
        c.pack()



tk = Tk()
c=custom_canvas(tk, width=100, height=200, highlightthickness=0)
m = MenuScreen
c.show_screen(m)
tk.mainloop()

