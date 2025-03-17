import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import time
import pygame
import threading
import struct
import ctypes
import os
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Get absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(script_dir, "./assets/bg.png")
gif_paths = [
    os.path.join(script_dir, "./assets/roll2.gif"),
    os.path.join(script_dir, "./assets/bounce.gif"),
    os.path.join(script_dir, "./assets/circle.gif"),
    os.path.join(script_dir, "./assets/random2.gif")
]
audio_path = os.path.join(script_dir, "./assets/lol.mp3")

# Function to change the desktop background
def changeBG(path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)

changeBG(bg_path)

# Initialize the tkinter window
root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', 1)
root.configure(bg='black')

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load GIFs
class AnimatedGIF:
    def __init__(self, gif_path, movement_func):
        self.original_gif = Image.open(gif_path)
        self.gif_width, self.gif_height = self.original_gif.size
        self.resize_factor = 0.5  # Adjust size if needed
        self.new_size = (int(self.gif_width * self.resize_factor), int(self.gif_height * self.resize_factor))
        self.frames = [ImageTk.PhotoImage(frame.resize(self.new_size)) for frame in ImageSequence.Iterator(self.original_gif)]
        self.label = tk.Label(root, bg='black')
        self.label.pack()
        self.movement_func = movement_func
        self.x, self.y = random.randint(0, screen_width - self.new_size[0]), random.randint(0, screen_height - self.new_size[1])
        self.dx, self.dy = 5, 5  # For bouncing
        self.angle = 0  # For circular motion
        self.update_gif()
        threading.Thread(target=self.movement_func, daemon=True).start()
    
    def update_gif(self, frame_index=0):
        self.label.config(image=self.frames[frame_index])
        root.after(50, self.update_gif, (frame_index + 1) % len(self.frames))

# Movement functions
def move_random(obj):
    while True:
        obj.x = random.randint(0, screen_width - obj.new_size[0])
        obj.y = random.randint(0, screen_height - obj.new_size[1])
        obj.label.place(x=obj.x, y=obj.y)
        time.sleep(0.5)

def move_bounce(obj):
    while True:
        obj.x += obj.dx
        obj.y += obj.dy
        if obj.x <= 0 or obj.x >= screen_width - obj.new_size[0]:
            obj.dx *= -1
        if obj.y <= 0 or obj.y >= screen_height - obj.new_size[1]:
            obj.dy *= -1
        obj.label.place(x=obj.x, y=obj.y)
        time.sleep(0.02)

def move_circle(obj):
    radius = 100
    center_x, center_y = screen_width // 2, screen_height // 2
    while True:
        obj.angle += 5
        obj.x = center_x + radius * math.cos(math.radians(obj.angle))
        obj.y = center_y + radius * math.sin(math.radians(obj.angle))
        obj.label.place(x=int(obj.x), y=int(obj.y))
        time.sleep(0.02)

def move_random2(obj):
    while True:
        obj.x += random.choice([-10, 10])
        obj.y += random.choice([-10, 10])
        obj.label.place(x=max(0, min(obj.x, screen_width - obj.new_size[0])),
                        y=max(0, min(obj.y, screen_height - obj.new_size[1])))
        time.sleep(0.1)

# Create GIF objects
gif1 = AnimatedGIF(gif_paths[0], move_random)
gif2 = AnimatedGIF(gif_paths[1], move_bounce)
gif3 = AnimatedGIF(gif_paths[2], move_circle)
gif4 = AnimatedGIF(gif_paths[3], move_random2)

# Function to keep the window on top
def bring_to_front():
    while True:
        root.lift()
        root.attributes('-topmost', 1)
        time.sleep(0.1)

threading.Thread(target=bring_to_front, daemon=True).start()

# Start the main GUI loop
root.mainloop()
