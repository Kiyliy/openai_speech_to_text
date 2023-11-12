#通过随机的方式获取api_key, 这样可以尽可能白嫖
import random
import logging
import os
import json

#环境变量
config_file = "config.json"


#API和URL变量
def set_api_data(key, api_url):
    global api_key, url
    api_key = key
    url = api_url

# API和URL变量
api_key = []
url = ""

#从配置文件加载API和URL
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            # 读取文件内容
            content = f.read()
            # 如果文件不是空的，则解析内容
            if content:
                try:
                    config = json.loads(content)
                    #key是一个列表
                    key = config.get('api_key', [])
                    set_api_data(key, config.get('url', ''))
                except json.JSONDecodeError as e:
                    logging.error(f"配置文件解析错误: {e}")
                    set_api_data('', '')  # 使用默认值或者留空
            else:
                logging.info("配置文件为空，使用默认配置")
                set_api_data('', '')  # 使用默认值或者留空
    else:
        logging.info("配置文件不存在，使用默认配置")
        set_api_data('', '')  # 使用默认值或者留空

# 保存API和URL到配置文件
def save_config(api_key, url):
    # 检查api_key是否已经是列表，如果不是，则将尝试分割,然后转换为列表
    if not isinstance(api_key, list):
        api_key = api_key.split(',')  # 将单个API密钥转换为列表

    # 保存配置文件
    with open(config_file, 'w') as f:
        json.dump({'api_key': api_key, 'url': url}, f)

#随机返回一个key
def get_api_key():
    return random.choice(api_key)

#返回url
def get_api_url():
    return url