from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.image import Image as coreImage
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle
import random
import numpy as np

images = ["Chrysanthemum.jpg", "Desert.jpg", "Hydrangeas.jpg", "Jellyfish.jpg", "Koala.jpg", "Lighthouse.jpg", "Penguins.jpg", "Tulips.jpg"]
difficulty_numbers = {"easy": 3, "medium": 6, "hard": 10, "very hard": 15, "insane": 21, "impossible": 28} # every difficulty translated to numbers


class Small_Image(ButtonBehavior, Image): # DONT SWITCH BUTTONBEHAVIOR AND IMAGE
    def __init__(self, texture, **kwargs):
        self.texture = texture
        self.selected = False
        self.ssos = .8 # ShrimpSizeOnSelect
        super().__init__(**kwargs)

    def get_rectangle(self):
        # the canvas class has some child widgets. The use of ids is not possible so this is the fastest way to get the Rectangle class
        rect = [child for child in self.canvas.children if isinstance(child, Rectangle)][0]
        return rect

    def update_texture(self, new_texture):
        rect = self.get_rectangle()
        rect.texture = new_texture # update the texture
        self.texture = new_texture # this makes it easier and faster to check if the image is correct

    def select(self):
        self.canvas.opacity = 0.65
        rect = self.get_rectangle()
        rect.size = tuple(np.array(rect.size) * self.ssos) # shrimp the image (to see its selected)
        rect.pos = self.x + ((1 - self.ssos) / 2) * (self.width), self.y + ((1 - self.ssos) / 2) * (self.height) # this centers the image when its shrimped
        self.selected = True

    def deselect(self):
        self.canvas.opacity = 1
        rect = self.get_rectangle()
        rect.size = tuple(np.array(rect.size) * (1/.8))
        rect.pos = self.x, self.y
        self.selected = False

    def on_press(self):
        if not self.selected: self.select()
        else: self.deselect()


class Game_Screen(Screen):
    imagebox_scale = NumericProperty(0.8)
    imagebox_aspect_ratio = NumericProperty(771/1024)

    def __init__(self, difficulty, **kwargs):
        self.difficulty = difficulty; self.diff_number = difficulty_numbers[self.difficulty]
        imagepath = "images/" + random.choice(images) # choosing a random image
        self.full_texture = coreImage(imagepath).texture # the whole image
        self.texture_list = [] # a list of all the textures for the smaller images
        #self.small_image_list = [] # a list of all the Small_Image instances

        super().__init__(**kwargs)
        Window.bind(on_resize=self.resize_imagebox)
        #Window.bind(on_mouse_up=self.testfunction)
        self.fill_texture_list()
        self.show_images()

    def testfunction(self, window, x, y, mouse_side, _):
        print(x, y, mouse_side, _)
        sil = self.ids.imagebox.children # Small_Image_List
        #print(sil[0].width, sil[0].height)
        #print(window.width, window.height)
        #for si in sil:
            #print(si.x, si.y)
        #print(sil[0].x, sil[0].y, sil[0].width, sil[0].height)
        #print(window.height)
        sil[0].update_texture(sil[1].texture)
        print(sil[0].canvas.children)

    def on_kv_post(self, base_widget): # setting the right size for the imagebox when we enter the screen
        self.resize_imagebox(Window, Window.width, Window.height)

    def resize_imagebox(self, window, width, height): # this will give the imagebox the right size when we resize the window
        imagebox = self.ids.imagebox
        imagebox.width = width * self.imagebox_scale
        imagebox.height = imagebox.width * self.imagebox_aspect_ratio
        imagebox.center_y = .5

    def fill_texture_list(self):
        width = self.full_texture.width; height = self.full_texture.height
        small_width = width/self.diff_number; small_height = height/self.diff_number # the width/height of an image part
        for x in np.arange(0, width, small_width):
            for y in np.arange(0, height, small_height):
                small_texture = self.full_texture.get_region(x, y, small_width, small_height)
                self.texture_list.append(small_texture)

        random.shuffle(self.texture_list)

    def show_images(self):
        for texture in self.texture_list:
            i = Small_Image(texture)
            self.ids.imagebox.add_widget(i)