import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_gigachat import GigaChat

load_dotenv()

model = GigaChat(
    credentials=os.environ.get("GIGACHAT_KEY"),
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    streaming=False,
    verify_ssl_certs=False,
)


def make_request_to_gigachat(prompt: str) -> str:
    messages = [
        HumanMessage(content=prompt)
    ]
    answer = model.invoke(messages)
    return answer.content


def get_advice(sex: str, age: int, height: int, weight: int, aim: str, condition: str, previous_trainings: str) -> str:
    sex_decoder = {"male": "мусжкой", "female": "женский"}
    prompt = (f"Мой пол: {sex_decoder[sex]}\nМой возраст: {age}\nМой рост: {height}\nМой вес: {weight}\nМоя цель "
              f"тренировок и опыт: {aim}\nМое физическое состояние на данный момент: {condition}\n Мои предыдущие "
              f"тренировки:\n{previous_trainings}\n Составь мне план из 5 тренировок, учитывая мое физическое "
              f"состояние, цель, опыт и другие описанные признаки.")
    return make_request_to_gigachat(prompt).replace("#", "")


def check_aim(aim: str) -> bool:
    prompt = (f"{aim}\n\nЕсли данный текст содержит в себе цель для тренировок и опыт тренировок (должен содержать "
              f"оба пункта), то напиши в ответе \"ДА\", в ином случае напиши в ответе \"НЕТ\", никаких других символов "
              f"в ответе быть не должно!")
    answer = make_request_to_gigachat(prompt)
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


def check_conditions(conditions: str) -> bool:
    prompt = (f"{conditions}\n\nЕсли данный текст содержит в себе физическое состояние человека, то напиши в ответе "
              f"\"ДА\", в ином случае напиши в ответе \"НЕТ\", никаких других символов в ответе быть не должно!")
    answer = make_request_to_gigachat(prompt)
    return "да" in answer.lower()


def text_with_trainings(trainings: list) -> str:
    trainings_str = ""
    for training in trainings:
        trainings_str += f"{training.type} - {training.time}\n"
    return trainings_str


def time2minutes(time: str) -> int:
    hours, minutes = (int(x) for x in time.split(":"))
    return hours * 60 + minutes


def minutes2time(minutes: int) -> str:
    hours = minutes // 60
    minutes = minutes % 60
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    else:
        hours = str(hours)
    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    return f"{hours}:{minutes}"
