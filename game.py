import pygame.mixer
from gpiozero import Button
import random
import os
import time
import requests
import threading

# Initialize Pygame mixer
pygame.mixer.init()

# Define the folder where your sound files are stored
sound_folder_fixed = "/home/alegria/alegria/sounds/fixe/"
sound_folder_random = "/home/alegria/alegria/sounds/random/"

# Get a list of sound files in the random folder
random_sounds = [os.path.join(sound_folder_random, file) for file in os.listdir(sound_folder_random) if file.endswith('.wav')]

# Define the buttons and the pins they're connected to
button_blue = Button(4, pull_up=True, bounce_time=0.2)  # GPIO 4 for blue button
button_red = Button(17, pull_up=True, bounce_time=0.2)  # GPIO 17 for red button
button_yellow = Button(27, pull_up=True, bounce_time=0.2)  # GPIO 27 for yellow button

current_sound = None
sound_thread = None  # Thread to handle sound playing
interrupt = False  # Flag to handle button press interruptions

# WLED device info
wled_ip = 'wled-b603a8.local'

def play_sound(sound_file):
    global current_sound
    if current_sound:
        current_sound.stop()  # Stop the current sound if it's playing
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
    current_sound = sound

def call_wled_preset(preset_number):
    try:
        url = f"http://{wled_ip}/win&PL={preset_number}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Preset {preset_number} called successfully!")
        else:
            print(f"Failed to call preset: {response.status_code}")
    except Exception as e:
        print(f"Error calling WLED preset: {e}")

def return_to_nominal():
    print("Returning to nominal state (Preset 2, croisiere.wav)")
    call_wled_preset(2)
    play_sound(os.path.join(sound_folder_fixed, "croisiere.wav"))

def handle_sound_playback(sound_file):
    global interrupt
    play_sound(sound_file)

    # Boucle pour vérifier si le son est en cours de lecture et revenir à l'état nominal à la fin
    while pygame.mixer.get_busy():
        if interrupt:  # If interrupted, stop the current sound and exit
            return
        time.sleep(0.1)

    return_to_nominal()  # Return to nominal state after the sound ends

def button_pressed(preset_number):
    global interrupt, sound_thread

    # Mark as interrupted if another sound is playing
    interrupt = True

    # Stop the sound thread if it's running
    if sound_thread and sound_thread.is_alive():
        sound_thread.join()  # Wait for the current sound thread to finish

    # Reset the interrupt flag for the new sound
    interrupt = False

    # Appel du preset approprié
    call_wled_preset(preset_number)

    # Jouer un son aléatoire dans un nouveau thread
    sound_file = random.choice(random_sounds)
    sound_thread = threading.Thread(target=handle_sound_playback, args=(sound_file,))
    sound_thread.start()

# Assign button press functions to the buttons
button_blue.when_pressed = lambda: button_pressed(10)
button_red.when_pressed = lambda: button_pressed(20)
button_yellow.when_pressed = lambda: button_pressed(30)

# Lancement initial : preset 2 et son croisiere.wav
print("Starting in nominal state (Preset 2, croisiere.wav)")
call_wled_preset(2)
play_sound(os.path.join(sound_folder_fixed, "croisiere.wav"))

try:
    while True:
        time.sleep(1)  # Main loop runs indefinitely

except KeyboardInterrupt:
    print("KeyboardInterrupt detected. Calling preset 'Off'.")
    call_wled_preset(1)

finally:
    pygame.mixer.quit()
    print("Exiting program.")

