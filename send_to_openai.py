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

logging.basicConfig(level=logging.INFO)


def send_to_openai_api(api_key,url,audio_file_path)->str:
    if not api_key or not url:
        raise ValueError("API密钥和URL必须设置")
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    with open(audio_file_path, 'rb') as audio_file:
        files = {'file': audio_file}
        try:
            response = requests.post(
                url=url,
                headers=headers,
                files=files,
                data={
                    'model': 'whisper-1',
                    "language": "zh",
                    "prompt": "respond in simplified Chinese"
                    },
                timeout = 60 # 超时时间   
            )
        except Exception as e:
            logging.error(e)
            return

    if response.status_code == 200:
        transcription = response.json()['text']
        print("转录文本:", transcription)
        logging.info("转录文本: %s\n", transcription)
        return transcription
    else:
        print("转录失败:", response.text)

#模拟按键操作: 复制粘贴文本
def paste_text(transcription):
        # 复制文本到剪贴板
        pyperclip.copy(transcription)
        # 模拟按键粘贴文本
        pyautogui.hotkey('ctrl', 'v')