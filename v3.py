import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import time
import pygame
import threading
import ctypes
import os
import math
import pyautogui
from contextlib import suppress

# Initialize pygame for sound
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
root.configure(bg='black')

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load GIFs
class AnimatedGIF:
    def __init__(self, gif_path, movement_func):
        try:
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
            threading.Thread(target=self.movement_func, args=(self,), daemon=True).start()
        except Exception as e:
            print(f"Error loading GIF {gif_path}: {e}")
    
    def update_gif(self, frame_index=0):
        self.label.config(image=self.frames[frame_index])
        root.after(50, self.update_gif, (frame_index + 1) % len(self.frames))

# Mouse jiggle function
def ghost_move():
    while True:
        current_pos = pyautogui.position()
        angle = math.radians(random.randint(-10, 10))
        new_x = max(0, min(screen_width - 1, current_pos[0] + int(10 * math.cos(angle))))
        new_y = max(0, min(screen_height - 1, current_pos[1] + int(10 * math.sin(angle))))
        pyautogui.moveTo(new_x, new_y, duration=0.2)
        time.sleep(2)

# Flash window function
def flash_window(duration=500):
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        with suppress(Exception):
            for _ in range(3):
                ctypes.windll.user32.FlashWindow(hwnd, True)
                time.sleep(duration / 1000)
                ctypes.windll.user32.FlashWindow(hwnd, False)
    except Exception as e:
        print(f"Error flashing window: {e}")

# Movement functions
def move_pygame_bounce(obj):
    while True:
        obj.x += obj.dx
        obj.y += obj.dy
        if obj.x <= 0 or obj.x >= screen_width - obj.new_size[0]:
            obj.dx *= -1
        if obj.y <= 0 or obj.y >= screen_height - obj.new_size[1]:
            obj.dy *= -1
        obj.label.place(x=obj.x, y=obj.y)
        time.sleep(0.02)

def move_pygame_circle(obj):
    radius = 100
    center_x, center_y = screen_width // 2, screen_height // 2
    while True:
        obj.angle += 5
        obj.x = center_x + radius * math.cos(math.radians(obj.angle))
        obj.y = center_y + radius * math.sin(math.radians(obj.angle))
        obj.label.place(x=int(obj.x), y=int(obj.y))
        time.sleep(0.02)

def move_pygame_random(obj):
    while True:
        obj.x += random.randint(-10, 10)
        obj.y += random.randint(-10, 10)
        obj.label.place(x=max(0, min(obj.x, screen_width - obj.new_size[0])),
                        y=max(0, min(obj.y, screen_height - obj.new_size[1])))
        time.sleep(0.1)

# Create GIF objects
gif1 = AnimatedGIF(gif_paths[0], move_pygame_random)
gif2 = AnimatedGIF(gif_paths[1], move_pygame_bounce)
gif3 = AnimatedGIF(gif_paths[2], move_pygame_circle)
gif4 = AnimatedGIF(gif_paths[3], move_pygame_random)

# Start ghost mouse movement in a separate thread
threading.Thread(target=ghost_move, daemon=True).start()

# Function to keep the window on top
def bring_to_front():
    root.lift()
    root.after(100, bring_to_front)

bring_to_front()

# Keybinding to exit program
def exit_program(event):
    root.destroy()

root.bind("<Escape>", exit_program)
root.bind("<Control-q>", exit_program)

# Start the main GUI loop
root.mainloop()

