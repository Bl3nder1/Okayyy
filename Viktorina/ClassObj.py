from aiogram.dispatcher.filters.state import State, StatesGroup

class Question(StatesGroup):
    question = State()
    ans1 = State()
    ans2 = State()
    ans3 = State()
    ans4 = State()
    photo = State()

    ans1_ob = State()
    ans2_ob = State()
    ans3_ob = State()
    ans4_ob = State()

    count_ans = State()