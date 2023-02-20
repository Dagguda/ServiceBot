from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from . import models


def number_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True) # Пространсво для кнопок

    # Сама кнопка
    phone_number = KeyboardButton('Поделиться контактом', request_contact=True)

    kb.add(phone_number)

    return kb


# Кнопки для выбора услуг
def send_service_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    all_services = models.Service.objects.all()

    for i in all_services:
        kb.add(i.service_name)

    return kb



