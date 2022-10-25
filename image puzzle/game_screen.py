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
        self.texture = new_texture # this makes it easier and faster to get the images texture

    def select(self):
        if self.selected: return
        self.canvas.opacity = 0.65
        rect = self.get_rectangle()
        rect.size = tuple(np.array(rect.size) * self.ssos) # shrimp the image (to see its selected)
        rect.pos = self.x + ((1 - self.ssos) / 2) * (self.width), self.y + ((1 - self.ssos) / 2) * (self.height) # this centers the image when its shrimped
        self.selected = True

    def deselect(self):
        if not self.selected: return
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
        self.small_images = [] # a list of all the Small_Image instances

        super().__init__(**kwargs)
        Window.bind(on_resize=self.resize_imagebox)
        self.keyboard = Window.request_keyboard(self.on_key_down, self)
        self.keyboard.bind(on_key_down=self.on_key_down) # when keyboard is pressed self.on_key_down will be fired
        self.fill_texture_list()
        self.show_images()

    def on_key_down(self, key, scancode, codepoint, modifier):
        keystring = scancode[1]
        if keystring in ("up", "down", "left", "right"):
            self.move_small_images(keystring)
        if keystring == 'r':
            self.swap_images()
        if keystring == "enter":
            self.deselect_all()

    def deselect_all(self):
        for small_image in self.small_images:
            small_image.deselect()


    ''' goal of this function: not actually move the image (becuz you cant insert things in kivy gridlayouts) on the screen but trade textures with the image you want to move to and then select that image
        imagebox:   Image 0   Image 1   Image 2
                    Image 3   Image 4   Image 5
                    Image 6   Image 7   Image 8
        if we want to move the image with index 8 above it needs to switch textures with the image with index 5
        then we deselect the image with index 8 and we select the image with index 5
    '''
    def move_small_images(self, direction):
        selected_images = [small_image for small_image in self.small_images if small_image.selected] # a list of the selected images
        indices_selected_images = [self.small_images.index(small_image) for small_image in selected_images] # the indices of the selected images in  self.small_images
        index_add_number = {"up": -self.diff_number, "down": +self.diff_number, "left": -1, "right": +1} # if we add this number to the index we get the image we want to move to
        target_indices = list(map(lambda index: index + index_add_number[direction], indices_selected_images)) # the indices we want to "move to"

        for target_index in target_indices:
            if target_index >= len(self.small_images) or target_index < 0: # index is out of borders so we dont move the images
                return None
        target_images = [self.small_images[target_index] for target_index in target_indices]

        # when we move to the right we need to move the most right image first. Try to imagine what happens if Image 6,7 are selected and we move first image 6 to the right. Same goes for down
        if direction in ("right", "down"):
            target_images.reverse()
            selected_images.reverse()

        for n, selected_image in enumerate(selected_images):
            # get textures
            target_image_texture = target_images[n].texture
            selected_image_texture = selected_image.texture
            # swap textures
            target_images[n].update_texture(selected_image_texture)
            selected_image.update_texture(target_image_texture)
            # swap selection
            selected_image.deselect()
            target_images[n].select()

    def swap_images(self):
        selected_images = [small_image for small_image in self.small_images if small_image.selected] # a list of the selected images
        if not len(selected_images) == 2: return None # this function is only possible when two images are selected
        texture_0 = selected_images[0].texture; texture_1 = selected_images[1].texture
        selected_images[0].update_texture(texture_1)
        selected_images[1].update_texture(texture_0)

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
            self.small_images.append(i)
            self.ids.imagebox.add_widget(i)
