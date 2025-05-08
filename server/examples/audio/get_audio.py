# -*- coding: utf-8 -*-
import os
import sys

# Locate the config file dynamically
sys.path.insert(0, os.getcwd())

from config import *

import time
import wave
import numpy as np
from naoqi import ALProxy
import paramiko
import os
import sys
import pygame


REMOTE_PATH = "/home/nao/recording.wav"  # Opravená cesta na robotu
LOCAL_PATH = "recording.wav"  # Uložení do aktuálního adresáře


def record_audio_on_nao():
    audio.startMicrophonesRecording(REMOTE_PATH, "wav", 16000, [1, 0, 0, 0])
    print("Recording...")
    time.sleep(0.3)
    audio.stopMicrophonesRecording()
    print("Recording finished.")

def download_file_from_nao():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, username="nao", password="nao")
    sftp = ssh.open_sftp()
    sftp.get(REMOTE_PATH, LOCAL_PATH)  # Stáhnutí souboru do aktuálního adresáře
    sftp.close()
    ssh.close()
    print("Downloaded: {}".format(LOCAL_PATH))

def parse_wav_to_numpy():
    wf = wave.open(LOCAL_PATH, 'rb')
    rate = wf.getframerate()
    frames = wf.getnframes()
    data = wf.readframes(frames)
    wf.close()
    samples = np.fromstring(data, dtype=np.int16)
    print("Parsed WAV: {} samples at {} Hz".format(len(samples), rate))
    return samples, rate

def play_audio():
    # Přehrání WAV souboru
    pygame.mixer.music.load(LOCAL_PATH)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Čeká, dokud není přehrávání hotové
        time.sleep(0.1)
    pygame.mixer.music.unload()

def main_loop():
    print("Starting main loop. Press Ctrl+C to stop.")
    try:
        while True:
            try:
                record_audio_on_nao()
                download_file_from_nao()
                # samples, rate = parse_wav_to_numpy()
                # print("Mean:", np.mean(samples))
                play_audio()  # Přehrání audio po každém záznamu
            except Exception as e:
                print("Error: {}".format(e))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        audio.stopMicrophonesRecording() 
        sys.exit(0)

if __name__ == "__main__":
    audio = ALProxy("ALAudioRecorder", IP, PORT)
    # Inicializace pygame pro přehrávání
    pygame.mixer.init()
    main_loop()
