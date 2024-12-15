import time
from plyer import notification
import pygame
from datetime import datetime
import random

reminder_count = 0

def get_random_message():
    messages = [
        "Stay hydrated! Drink some water! 💧",
        "Your body needs water! Drink up! 🌊",
        "Don't forget to hydrate, it's important! 💦",
        "Drink water, it's great for your skin and energy! ✨",
        "Time to hydrate! Your body will thank you! 😄"
    ]
    return random.choice(messages)

def log_reminder():
    with open("hydration_log.txt", "a") as log_file:
        log_file.write(f"Reminder sent at {datetime.now()}\n")

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("MGS_Alert.mp3")  
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def remind_to_drink():
    global reminder_count
    while True:
        reminder_count += 1

        message = get_random_message()

        notification.notify(
            title=f"Hydration Reminder {reminder_count}",
            message=message,
            app_name="Drink Reminder",
            timeout=10
        )

        log_reminder()

        play_sound()

        time.sleep(15 * 60)

if __name__ == "__main__":
    remind_to_drink() 
