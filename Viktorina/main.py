from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from cfg import *
import urllib.parse
from ClassObj import *
from aiogram.dispatcher.filters import Text
from keyboard import *
import json
from alldef import *

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=["start"])
async def echo(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(text="Привет!\n"
                                  "Выбери то что тебя интересует!", reply_markup=Menu)


@dp.message_handler(text='Добавить задачу')
async def echo(message: types.Message):
    await message.answer(text="Отлично! Давай созданим новый вопрос!")
    await message.answer(text="Для начала введи вопрос!", reply_markup=Stop)
    await Question.next()

@dp.message_handler(state=Question.question)
async def echo(message: types.Message, state: FSMContext):
    q = message.text
    if q == "Назад":
        await message.answer(text="Выбери то что тебя интересует!", reply_markup=Menu)
        await state.finish()
    else:
        Question.question = q
        await message.answer(text="Хорошо. Теперь теперь введи первый вариант ответа\n"
                                  "Первыйе два варианта обязательны! От остальных сможешь отказаться\n"
                                  "Через '|' введи объяснение")
        await Question.next()

@dp.message_handler(state=Question.ans1)
async def echo(message: types.Message, state: FSMContext):
    ans = message.text
    ans = ans.split('|')
    Question.ans1 = ans[0]
    Question.ans1_ob = ans[1]
    Question.count_ans = 1
    await Question.next()
    await message.answer(text="Второй вариант!")

@dp.message_handler(state=Question.ans2)
async def echo(message: types.Message, state: FSMContext):
    ans = message.text
    ans = ans.split('|')
    Question.ans2 = ans[0]
    Question.ans2_ob = ans[1]
    Question.count_ans = 2
    await Question.next()
    await message.answer(text='Третий вариант! Что бы отказаться, введи "-"')
    print("0")

@dp.message_handler(state=Question.ans3)
async def echo(message: types.Message, state: FSMContext):
    ans = message.text
    if ans == '-':
        await Question.next()
        await message.answer(text='Хорошо. Отказались, введите еще один "-"')
        Question.ans3 = '-'
        print("1")
    else:
        ans = ans.split('|')
        Question.ans3 = ans[0]
        Question.ans3_ob = ans[1]
        Question.count_ans = 3
        await Question.next()
        await message.answer(text='Четвертый вариант! Что бы отказаться, введи "-"')
        print("2")

@dp.message_handler(state=Question.ans4)
async def echo(message: types.Message, state: FSMContext):
    print(Question.ans3)
    if Question.ans3 != '-':
        ans = message.text
        if ans != '-':
            ans = ans.split('|')
            Question.ans4 = ans[0]
            Question.ans4_ob = ans[1]
            Question.count_ans = 4
        else:
            Question.ans4 = '-'
    else:
        Question.ans4 = '-'

    await message.answer(text='Что бы добавить фото, отправьте фото')
    await Question.next()

@dp.message_handler(state=Question.photo, content_types=types.ContentTypes.ANY)
async def echo(message: types.Message, state: FSMContext):
    if message.photo:
        fileID = message.photo[-1].file_id
        listANS = [Question.ans1, Question.ans2, Question.ans3, Question.ans4]
        listOB = [Question.ans1_ob, Question.ans2_ob, Question.ans3_ob, Question.ans4_ob]
        add_task(Question.question, listOB, listANS, fileID, Question.count_ans)
        await state.finish()

        with open("Viktorina.json", "r", encoding="utf-8") as f:
            data = json.load(f)

            user_data = data.get(Question.question[-6:], {})

            ques = user_data.get('question')
            photo = user_data.get('PhotoID')


        if photo:
            await bot.send_photo(chat_id=Chat_Id, photo=photo, caption=f'{ques}',
                                 reply_markup=kpk(Question.count_ans, Question.question))
        else:
            await bot.send_message(chat_id=Chat_Id, text=f'{ques}',
                                    reply_markup=kpk(Question.count_ans, Question.question))
    else:
        await message.answer(text=f"Вы отправили что-то не то.")






@dp.callback_query_handler(Text(startswith='answer'))
async def ansecho(call: types.CallbackQuery, state: FSMContext):
    # Проверяем подписку на канал перед обработкой ответа
    user_channel_status = await bot.get_chat_member(chat_id=Chat_Id, user_id=call.from_user.id)
    if user_channel_status["status"] == 'left':
        await call.answer("Чтобы ответить, подпишитесь на наш канал: https://t.me/ваш_канал", show_alert=True)
    else:

        cb = call.data.split('_')
        with open("Viktorina.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            user_data = data.get(cb[-1], {})

            listOB = user_data.get('OB')
            la = user_data.get("YesAns")
            allus = user_data.get("all")
            corus = user_data.get("correct")

        indexx = int((cb[1]))
        if call.from_user.id not in la:
            with open('Viktorina.json', 'r', encoding='utf-8') as f:
                obj = json.load(f)
                tmp1 = obj[cb[-1]]["all"] + 1
                tmp2 = obj[cb[-1]]["correct"]
                tmp2[int(cb[1])] += 1
                tmp3 = obj[cb[-1]]["YesAns"]
            tmp3.append(call.from_user.id)

            update_json('Viktorina.json', cb[-1], 'all', tmp1)
            update_json('Viktorina.json', cb[-1], 'correct', tmp2)
            update_json('Viktorina.json', cb[-1], "YesAns", tmp3)
            print('accept')

        try:
            with open("Viktorina.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                user_data = data.get(cb[-1], {})

                listOB = user_data.get('OB')
                la = user_data.get("YesAns")
                allus = user_data.get("all")
                corus = user_data.get("correct")

            p = '{:.2f}'.format(((corus[int(cb[1])])/allus)*100)
            await call.answer(text=f'{listOB[indexx]}\n\n'
                                    f'Ответили так же: {corus[int(cb[1])]} чел. ({p}%)', show_alert=True)
            print('ansaccept')
        except:
            pass





















if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)