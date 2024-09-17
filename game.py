import pygame.mixer
from gpiozero import Button
import random
import os
import time
import requests
import threading

# Initialize Pygame mixer
pygame.mixer.init()

# Define the folders where your sound files are stored
sound_folder_nominal = "/home/alegria/alegria/sounds/attente/"
sound_folder_moulinette = "/home/alegria/alegria/sounds/moulinette/"
sound_folder_win = "/home/alegria/alegria/sounds/gagné/"
sound_folder_lose = "/home/alegria/alegria/sounds/perdu/"

# Get a list of sound files in the respective folders
nominal_sounds = [os.path.join(sound_folder_nominal, file) for file in os.listdir(sound_folder_nominal) if file.endswith('.wav')]
moulinette_sounds = [os.path.join(sound_folder_moulinette, file) for file in os.listdir(sound_folder_moulinette) if file.endswith('.wav')]
win_sounds = [os.path.join(sound_folder_win, file) for file in os.listdir(sound_folder_win) if file.endswith('.wav')]
lose_sounds = [os.path.join(sound_folder_lose, file) for file in os.listdir(sound_folder_lose) if file.endswith('.wav')]

# Define the buttons and the pins they're connected to
button_blue = Button(27, pull_up=True, bounce_time=0.2)    # GPIO 4 for blue button
button_red = Button(22, pull_up=True, bounce_time=0.2)    # GPIO 17 for red button
button_yellow = Button(17, pull_up=True, bounce_time=0.2) # GPIO 27 for yellow button
button_win = Button(23, pull_up=True, bounce_time=0.2)    # GPIO 23 for pédale gagnée
button_lose = Button(24, pull_up=True, bounce_time=0.2)   # GPIO 24 for pédale perdue

current_sound = None
sound_thread = None  # Thread to handle sound playing
interrupt = False  # Flag to handle button press interruptions
can_return_to_nominal = True  # Flag to control when to return to nominal state

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
    global can_return_to_nominal
    if can_return_to_nominal:  # Only return to nominal if allowed
        print("Returning to nominal state (Preset 2, playing random attente sound)")
        call_wled_preset(2)
        play_sound(random.choice(nominal_sounds))

def handle_sound_playback(sound_file, return_nominal=True):
    global interrupt, can_return_to_nominal
    play_sound(sound_file)

    # Boucle pour vérifier si le son est en cours de lecture et revenir à l'état nominal à la fin
    while pygame.mixer.get_busy():
        if interrupt:  # If interrupted, stop the current sound and exit
            return
        time.sleep(0.1)

    if return_nominal:  # Return to nominal only if allowed
        return_to_nominal()

def button_pressed(preset_number, sound_list, return_nominal=True):
    global interrupt, sound_thread, can_return_to_nominal

    # Mark as interrupted if another sound is playing
    interrupt = True

    # Stop the sound thread if it's running
    if sound_thread and sound_thread.is_alive():
        sound_thread.join()  # Wait for the current sound thread to finish

    # Reset the interrupt flag for the new sound
    interrupt = False

    # Appel du preset approprié
    call_wled_preset(preset_number)

    # Désactiver le retour à l'état nominal si un son moulinette est joué
    if sound_list == moulinette_sounds:
        can_return_to_nominal = False
    else:
        can_return_to_nominal = True

    # Jouer un son aléatoire de la liste spécifiée dans un nouveau thread
    sound_file = random.choice(sound_list)
    sound_thread = threading.Thread(target=handle_sound_playback, args=(sound_file, return_nominal))
    sound_thread.start()

# Assign button press functions to the buttons
button_blue.when_pressed = lambda: button_pressed(10, moulinette_sounds, return_nominal=False)
button_red.when_pressed = lambda: button_pressed(20, moulinette_sounds, return_nominal=False)
button_yellow.when_pressed = lambda: button_pressed(30, moulinette_sounds, return_nominal=False)
button_win.when_pressed = lambda: button_pressed(5, win_sounds, return_nominal=True)
button_lose.when_pressed = lambda: button_pressed(6, lose_sounds, return_nominal=True)

# Lancement initial : preset 2 et son aléatoire dans le répertoire attente
print("Starting in nominal state (Preset 2, random attente.wav)")
call_wled_preset(2)
play_sound(random.choice(nominal_sounds))

try:
    while True:
        time.sleep(1)  # Main loop runs indefinitely

except KeyboardInterrupt:
    print("KeyboardInterrupt detected. Calling preset 'Off'.")
    call_wled_preset(1)

finally:
    pygame.mixer.quit()
    print("Exiting program.")

