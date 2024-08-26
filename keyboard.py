from aiogram.types import *
from ClassObj import *
import json

def kpk(a, name):
    with open("Viktorina.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        user_data = data.get(name[-6:], {})

        list = user_data.get("ANS")
    print(list,'????')
    print(a)


    BottonAns = InlineKeyboardMarkup(row_width=1)

    for i in range(a):
        BottonAns.add(InlineKeyboardButton(text=f'{list[i]}', callback_data=f'answer_{i}_{name[-6:]}'))

    return BottonAns



Menu = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='Добавить задачу')
Menu.add(b1)

Stop = ReplyKeyboardMarkup(resize_keyboard=True)
s1 = KeyboardButton(text='Назад')
Menu.add(s1)