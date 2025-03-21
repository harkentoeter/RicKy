import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import time
import pygame
import threading
import struct
import ctypes
import os
import pyautogui
import math

pygame.init()
pygame.mixer.init()

script_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(script_dir, "./assets/bg.png")
gif_path = os.path.join(script_dir, "./assets/roll2.gif")
audio_path = os.path.join(script_dir, "./assets/lol.mp3")

def changeBG(path):
    SPI_SETDESKWALLPAPER = 20
    try:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
        print("Wallpaper changed successfully!")
    except Exception as e:
        print(f"Error changing wallpaper: {e}")

changeBG(bg_path)

def play_music():
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.set_volume(1.0) 
        pygame.mixer.music.play(-1) 
        print("Music started successfully!")
    except Exception as e:
        print(f"Error playing music: {e}")

play_music()

root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', 1)
root.configure(bg='black')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

original_gif = Image.open(gif_path)
gif_width, gif_height = original_gif.size
resize_factor = 0.5 
new_size = (int(gif_width * resize_factor), int(gif_height * resize_factor))
frames = [ImageTk.PhotoImage(frame.resize(new_size)) for frame in ImageSequence.Iterator(original_gif)]

gif_label = tk.Label(root, bg='black')
gif_label.pack()

def update_gif(frame_index=0):
    gif_label.config(image=frames[frame_index])
    root.after(50, update_gif, (frame_index + 1) % len(frames))

update_gif()

def move_window():
    while True:
        window_x = random.randint(0, screen_width - new_size[0])
        window_y = random.randint(0, screen_height - new_size[1])
        root.geometry(f"{new_size[0]}x{new_size[1]}+{window_x}+{window_y}")
        time.sleep(0.1)

def bring_to_front():
    while True:
        root.lift()
        root.attributes('-topmost', 1)
        time.sleep(0.02)

def ghost_move():
    while True:
        current_pos = pyautogui.position()
        angle = math.radians(random.randint(-180, 180))  # Extreme unpredictable movement
        speed = random.randint(50, 200)  # Even larger jumps
        new_x = max(0, min(screen_width - 1, current_pos[0] + int(speed * math.cos(angle))))
        new_y = max(0, min(screen_height - 1, current_pos[1] + int(speed * math.sin(angle))))
        pyautogui.moveTo(new_x, new_y, duration=0.02)  # Insanely fast movement
        time.sleep(0.05)  # Almost no delay

threading.Thread(target=move_window, daemon=True).start()
threading.Thread(target=bring_to_front, daemon=True).start()
threading.Thread(target=ghost_move, daemon=True).start()

root.mainloop()
