from tkinter import *
from PIL import Image, ImageDraw
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2
import matplotlib.pyplot as plt

model = tf.keras.models.load_model('model')

def getNumber(img):
    image = np.asarray(img)
    image = image[:,:,0]
    # image = cv2.imread('image.png', 0)
    image = cv2.resize(image, (28,28))  
    image = 1 - (image / 255.0)
    
    image = image.astype('float32')

    prediction = model.predict(image.reshape(1, 28, 28, 1))
    return prediction.argmax()


class Board:
    def __init__(self,master):
        self.master = master
        self.old_x = None
        self.old_y = None
        self.penwidth = 35
        self.drawWidgets()
        self.state = False
        self.c.bind('<B1-Motion>',self.paint)
        self.c.bind('<ButtonRelease-1>',self.reset) 
        self.image = Image.new("RGB", (500, 500), "white")
        self.draw = ImageDraw.Draw(self.image)

    def paint(self,e):
        if self.state:
            self.clear()
            self.state=False
            self.draw.rectangle((0,0,500,500), fill=(255,255,255,1))

        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill='black',capstyle=ROUND,smooth=True)
            self.draw.line([self.old_x,self.old_y,e.x,e.y],fill="black",width=self.penwidth)
        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):
        self.state = True
        self.old_x = None
        self.old_y = None
        # self.image.save("image.png")
        print(getNumber(self.image))
    
    def clear(self):
        self.c.delete(ALL)

    def drawWidgets(self):
        self.c = Canvas(self.master,width=500,height=500,bg='white')
        self.c.pack(fill=BOTH,expand=True)
        
root = Tk()
Board(root)
root.title('Board')
root.mainloop()