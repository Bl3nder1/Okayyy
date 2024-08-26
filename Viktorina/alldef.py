import json


q_dict = {}

try:
    with open("Viktorina.json", "r", encoding="utf-8") as file:
        q_dict = json.load(file)
    print("Файл Viktorina.json найден.")
except FileNotFoundError:
    print("Файл Viktorina.json не найден. Создается новый файл.")
def add_task(question, ListOB, ListANS, photo_id, cot):
    Ob = []
    ans = []
    correct = []
    for i in range(cot):
        Ob.append(ListOB[i])
        ans.append(ListANS[i])
        correct.append(0)


    q_dict[question[-6:]] = {
        "question": question,
        "ANS": ans,
        "OB": Ob,
        "PhotoID": photo_id,
        "all": 0,
        "correct": correct,
        "YesAns": []
    }



    with open("Viktorina.json", "w", encoding="utf-8") as file:
        json.dump(q_dict, file, indent=4, ensure_ascii=False)



import json

def update_json(file_path, question_id, field, value):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return



    if question_id in data:
        data[question_id][field] = value
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Данные в вопросе {question_id} успешно обновлены.")
    else:
        print(f"Вопрос с ID {question_id} не найден в файле.")