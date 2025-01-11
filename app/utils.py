import datetime
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


def make_request(prompt: str) -> str:
    access_token = get_access_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {"role": "user",
             "content": prompt}
        ],
        "n": 1,
        "stream": False,
        "max_tokens": 10000,
        "repetition_penalty": 1,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    answer = \
        requests.request("POST", url, headers=headers, data=payload, verify=False).json()['choices'][0][
            'message']['content']
    return answer


def get_advice(sex: str, age: int, height: int, weight : int, aim : str, condition: str, previous_trainings: str) -> str:
    sex_decoder = {"male": "мусжкой", "female": "женский"}
    prompt = (f"Мой пол: {sex_decoder[sex]}\nМой возраст: {age}\nМой рост: {height}\nМой вес: {weight}\nМоя цель "
              f"тренировок и опыт: {aim}\nМое физическое состояние на данный момент: {condition}\n Мои предыдущие "
              f"тренировки:\n{previous_trainings}\n Составь мне план из 5 тренировок, учитывая мое физическое "
              f"состояние, цель, опыт и другие описанные признаки.")
    return make_request(prompt).replace("#", "")


def check_aim(aim: str) -> bool:
    prompt = (f"{aim}\n\nЕсли данный текст содержит в себе цель для тренировок и опыт тренировок (должен содержать "
              f"оба пункта), то напиши в ответе \"ДА\", в ином случае напиши в ответе \"НЕТ\", никаких других символов "
              f"в ответе быть не должно!")
    answer = make_request(prompt)
    return "да" in answer.lower()


def check_age(age: str) -> bool:
    if age.isnumeric():
        return 5 <= int(age) <= 70
    else:
        return False


def check_weight(weight: str) -> bool:
    if weight.isnumeric():
        return 20 <= int(weight) <= 250
    else:
        return False


def check_height(height: str) -> bool:
    if height.isnumeric():
        return 100 <= int(height) <= 300
    else:
        return False


def text_with_trainings(trainings: list) -> str:
    trainings_str = ""
    for training in trainings:
        trainings_str += f"{training.type} - {training.time}\n"
    return trainings_str
