import requests
import json
import logging


text = ""
prompt = f"""User
扮演语音转文字修复助手, 直接只给出结果, 下面是用户的转文字结果:
"""
{text}
""""""

def Chatfix(model,api_key,url,text):
    #兼容url
    def url_fix(url):
        if "v1" not in url:
            url = url+"/v1/chat/completions"
        elif "v1" in url and "chat" not in url:
            url = url+"/chat/completions"
        else:
            url = url
        return url

    url = url_fix(url)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+api_key
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt.format(text=text)}
        ],
        "temperature": 0.7,
        "max_tokens": None,
        # "stream": True
    }
    #请求返回
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        trans = response_data["choices"][0]["message"]["content"]
        logging.info(f"结果:{trans}")
        #尝试将其转换为json



        return trans
    except Exception:
        response_data = {"error":"error"}
        print(f"error:{url}")

    return response_data