import pyaudio
import wave
import requests
import json
import base64
import pyautogui
import threading
import logging
import pyperclip
from threading import Lock
import os
import random
import time
import get_api_key
from send_to_openai import send_to_openai_api , paste_text


logging.basicConfig(level=logging.INFO)

# 确保在模块加载时调用load_config
get_api_key.load_config()

# API和URL变量
api_key = get_api_key.get_api_key()
url = get_api_key.get_api_url()

# 录音参数
chunk = 1024
format = pyaudio.paInt16
channels = 1
rate = 44100

# 录音控制变量
is_recording = False
frames = []
frames_lock = Lock()

def start_recording():
    global is_recording
    with frames_lock:
        if not is_recording:
            is_recording = True
            frames.clear()
            threading.Thread(target=record).start()
        else:
            logging.info("录音已在进行中。")


def stop_recording():
    global is_recording
    with frames_lock:
        if is_recording:
            is_recording = False
        else:
            logging.info("录音已停止。")

def record():
    global frames
    logging.info("录音开始...")
    p = pyaudio.PyAudio()
    
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    try:
        while is_recording:
            data = stream.read(chunk)
            with frames_lock:
                frames.append(data)
    except Exception as e:
        logging.error(f"录音过程中出错: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        logging.info("录音结束...")
        save_recording(frames, p)

def save_recording(frames, audio):
    wf = wave.open('temp_audio.wav', 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    api_key = get_api_key.get_api_key()
    transcription= send_to_openai_api(api_key,url,'temp_audio.wav')
    paste_text(transcription)
    


if __name__ == "__main__":
    pass