# -*- coding: utf-8 -*-
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *

# -*- coding: utf-8 -*-
import time
import wave
from naoqi3 import ALProxy
import paramiko
import os
import sys
import pygame


REMOTE_PATH = "/home/nao/recording.wav" 
LOCAL_PATH = "recording.wav" 


def record_audio_on_nao():
    audio.startMicrophonesRecording(REMOTE_PATH, "wav", 16000, [1, 0, 0, 0])
    print("Recording...")
    time.sleep(0.5)
    audio.stopMicrophonesRecording()
    print("Recording finished.")


def download_file_from_nao():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, username="nao", password="nao")
    sftp = ssh.open_sftp()
    sftp.get(REMOTE_PATH, LOCAL_PATH)  # download file to current directory
    sftp.close()
    ssh.close()
    print("Downloaded: {}".format(LOCAL_PATH))


def play_audio():
    pygame.mixer.music.load(LOCAL_PATH)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # waits until playback is finished
        time.sleep(0.1)
    pygame.mixer.music.unload()


def main_loop():
    print("Starting main loop. Press Ctrl+C to stop.")
    try:
        while True:
            try:
                record_audio_on_nao()
                download_file_from_nao()
                play_audio()  # play the downloaded audio
            except Exception as e:
                print("Error: {}".format(e))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        audio.stopMicrophonesRecording()
        sys.exit(0)


if __name__ == "__main__":
    audio = ALProxy("ALAudioRecorder", IP, PORT)
    # init pygame for audio playback
    pygame.mixer.init()
    main_loop()
