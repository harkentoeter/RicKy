import os
import random
import time
import pygame
import threading
import ctypes
import struct
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# Initialize Pygame for sound
pygame.init()
pygame.mixer.init()

# Function to check Windows bit version
def is_64bit_windows():
    return struct.calcsize('P') * 8 == 64

# Function to change wallpaper
def changeBG(path):
    if is_64bit_windows():
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(20, 0, path, 3)

# Get paths to assets
script_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(script_dir, "./assets/bg.jpg")
gif_path = os.path.join(script_dir, "./assets/roll2.gif")
audio_path = os.path.join(script_dir, "./assets/lol.mp3")

# Change the desktop wallpaper
changeBG(bg_path)

# Load and play prank audio
if os.path.exists(audio_path):
    prank_sound = pygame.mixer.Sound(audio_path)
    prank_sound.set_volume(0.5)
    prank_sound.play(-1)  # Loop audio

# GUI Prank
root = tk.Tk()
root.overrideredirect(True)
root.attributes('-transparentcolor', 'white')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

canvas = tk.Canvas(root, width=110, height=120, highlightthickness=0, bg='black')
canvas.pack()

# Load GIF
rickroll_animation = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(rickroll_animation)]
gif_label = tk.Label(canvas, image=frames[0], background='black')
gif_label.pack()

# Function to animate GIF
def update_gif():
    frame_index = 0
    while True:
        frame_index = (frame_index + 1) % len(frames)
        gif_label.config(image=frames[frame_index])
        root.after(30, update_gif)

# Function to move window randomly
def move_window():
    while True:
        window_x = random.randint(0, screen_width - 110)
        window_y = random.randint(0, screen_height - 120)
        canvas.config(bg=f'#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}')
        root.geometry(f"+{window_x}+{window_y}")
        root.update()
        time.sleep(0.5)

# Function to keep prank window on top
def bring_to_front():
    while True:
        root.lift()
        root.attributes('-topmost', 1)
        time.sleep(0.1)

# Function to stop prank on exit
def stop_prank():
    print("Stopping prank...")
    prank_sound.stop()  # Stop audio
    root.destroy()  # Close GUI
    os._exit(0)  # Kill process

root.protocol("WM_DELETE_WINDOW", stop_prank)  # Stop prank when window is closed

# Start prank threads
threading.Thread(target=update_gif, daemon=True).start()
threading.Thread(target=move_window, daemon=True).start()
threading.Thread(target=bring_to_front, daemon=True).start()

root.mainloop()

