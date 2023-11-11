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



logging.basicConfig(level=logging.INFO)

#环境变量
config_file = "config.json"

# API和URL变量
api_key = ""
url = ""

def set_api_data(key, api_url):
    global api_key, url
    api_key = key
    url = api_url

# 保存API和URL到配置文件
def save_config(api_key, url):
    with open(config_file, 'w') as f:
        json.dump({'api_key': api_key, 'url': url}, f)

# 从配置文件加载API和URL
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            # 读取文件内容
            content = f.read()
            # 如果文件不是空的，则解析内容
            if content:
                try:
                    config = json.loads(content)
                    set_api_data(config.get('api_key', ''), config.get('url', ''))
                except json.JSONDecodeError as e:
                    logging.error(f"配置文件解析错误: {e}")
                    set_api_data('', '')  # 使用默认值或者留空
            else:
                logging.info("配置文件为空，使用默认配置")
                set_api_data('', '')  # 使用默认值或者留空
    else:
        logging.info("配置文件不存在，使用默认配置")
        set_api_data('', '')  # 使用默认值或者留空


# 确保在模块加载时调用load_config
load_config()
# # OpenAI API key

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

    # 准备发送到OpenAI API
    send_to_openai_api('temp_audio.wav')

def send_to_openai_api(audio_file_path):
    if not api_key or not url:
        raise ValueError("API密钥和URL必须设置")
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    with open(audio_file_path, 'rb') as audio_file:
        files = {'file': audio_file}
        response = requests.post(
            url=url,
            headers=headers,
            files=files,
            data={
                'model': 'whisper-1',
                "language": "zh"
                }
        )

    if response.status_code == 200:
        transcription = response.json()['text']
        print("转录文本:", transcription)
        logging.info("转录文本: %s", transcription)
        # 复制文本到剪贴板
        pyperclip.copy(transcription)
        # 模拟按键粘贴文本
        pyautogui.hotkey('ctrl', 'v')
    else:
        print("转录失败:", response.text)

if __name__ == "__main__":
    pass