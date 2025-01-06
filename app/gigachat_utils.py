import json
import os
import uuid

import requests
from dotenv import load_dotenv


def get_access_token():
    load_dotenv()
    authorization_key = os.environ.get("GIGACHAT_KEY")
    auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    rq_uid = str(uuid.uuid4())
    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {authorization_key}'
    }
    access_token = requests.request("POST", auth_url, headers=headers, data=payload, verify=False).json()[
        'access_token']
    return access_token


def get_advice():
    access_token = get_access_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    prompt = "Как мне тренироваться, если я хочу накачаться. Ответь конкретно без лишних вопросов."
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {"role": "user",
             "content": prompt}
        ],
        "temperature": 0.5,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    advice = \
        requests.request("POST", url, headers=headers, data=payload, verify=False).json()['choices'][0][
            'message']['content']
    return advice
