import requests
import pyautogui
import logging
import pyperclip
from threading import Lock
from get_api_key import get_api_key

logging.basicConfig(level=logging.INFO)


def send_to_openai_api(api_key,url,audio_file_path)->str:
    print("DEBUD: api_key:",api_key)
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
            if response.status_code == 200:
                transcription = response.json()['text']
                print("转录文本:", transcription)
                logging.info("转录文本: %s\n", transcription)
                return transcription
            else:
                #如果rate_limit
                if(response.status_code == 429 and ("requests per day" in response.json()['error']['message']) ):
                    #临时删除这个key
                    import get_api_key
                    get_api_key.delete_key(api_key)
                    logging.info("API密钥已临时删除")
                print("转录失败:", response.text)

        except Exception as e:
            logging.error(e)
            return



#模拟按键操作: 复制粘贴文本
def paste_text(transcription):
        # 复制文本到剪贴板
        pyperclip.copy(transcription)
        # 模拟按键粘贴文本
        pyautogui.hotkey('ctrl', 'v')