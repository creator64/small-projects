from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import random
import numpy as np
import image_slicer

images = ["Chrysanthemum.jpg", "Desert.jpg", "Hydrangeas.jpg", "Jellyfish.jpg", "Koala.jpg", "Lighthouse.jpg", "Penguins.jpg", "Tulips.jpg"]
difficulty_numbers = {"easy": 5, "medium": 10, "hard": 15, "insane": 20, "impossible": 25} # every difficulty translated to numbers

class GameScreen:
    def __init__(self, canvas, difficulty):
        self.canvas = canvas
        self.difficulty = difficulty; self.diff_number = difficulty_numbers[self.difficulty]
        self.small_images = []
        self.imglabellist = []

        self.mainLabel = Label(canvas, text="IMAGEPUZZLER", font=("Courier", 25)); self.mainLabel.pack()

        imagepath = "images/" + random.choice(images) # choosing a random image
        self.imgpil = Image.open(imagepath); #img = ImageTk.PhotoImage(self.imgpil) # loading image
        #self.imglabel = Label(self.canvas, image=img) # the normal canvas.create_image doesnt work so well do it this way
        #self.imglabel.image = img # without this line of code the image wont show
        #self.imglabel.pack()
        self.create_image_parts()
        #self.show_images()

    def create_image_parts(self):
        width = self.imgpil.width; height = self.imgpil.height
        small_width = width/self.diff_number; small_height = height/self.diff_number # the width/height of an image part
        for x in np.arange(0, width, small_width):
            for y in np.arange(0, height, small_height):
                small_image = self.imgpil.crop((x, y, small_width, small_height))
                self.small_images.append(ImageTk.PhotoImage(small_image))
                
        random.shuffle(self.small_images)
        #self.small_images[0].show()

    def create_image_parts(self):
        imagepath = "images/" + random.choice(images) # choosing a random image
        tiles = image_slicer.slice(imagepath, 10, save=False)
        img = ImageTk.PhotoImage(tiles[0].image)
        imglabel = Label(self.canvas, image=img) # the normal canvas.create_image doesnt work so well do it this way
        imglabel.image = img # without this line of code the image wont show
        imglabel.place(x=0, y=0, width=100, height=100)
        img2 = ImageTk.PhotoImage(tiles[1].image)
        tiles[0].image.show()
        tiles[1].image.show()


    def show_images(self):
        width = self.imgpil.width; height = self.imgpil.height
        small_width = width/self.diff_number; small_height = height/self.diff_number # the width/height of an image part

        i = 0
        for x in np.arange(0, width, small_width):
            for y in np.arange(0, height, small_height):
                img = self.small_images[i]#; img = ImageTk.PhotoImage(imgpil)
                imglabel = Label(self.canvas, image=img) # the normal canvas.create_image doesnt work so well do it this way
                imglabel.image = img # without this line of code the image wont show
                imglabel.place(x=0, y=0, width=100, height=100)
                #self.imglabellist.append(imglabel)
                #self.canvas.pics.append(img)
                #self.canvas.create_image(x,y,image=img)
                i += 1
















    def win(self):
        pass
