from datetime import datetime
from pathlib import Path


def add_note(contacts, *args):
    """
    Зберігає нотатку за шляхом .\note_directory\note.txt в note.txt
    формат запису: DD.MM.YYYY - HH,MM,SS | Note
    """
    note = ' '.join(args)
    date_now = datetime.now()
    str_date_now = date_now.strftime("%d.%m.%Y - %H:%M:%S")
    with open(f"{Path().cwd()}/note_directory/note.txt", "a+", encoding='utf-8') as file:
        file.write(str_date_now + " | " + note + "\n")
    return "The note is added."


def find_note(contacts, *args):
    """
    Пошук за ключовим словом у нотатках + між датами створення
    """

    # розбираєм аргументи в форматі: keyword = keywords, start = start date, end = end date
    if len(args) >= 3:
        keyword = args[0].lower()
        start = args[1]
        end = args[2]
    elif len(args) == 2:
        keyword = args[0].lower()
        start = args[1]
        end = ''
    elif len(args) == 1:
        keyword = args[0].lower()
        start = ''
        end = ''
    else:
        keyword = ''
        start = ''
        end = ''
        print("Keyword not specified. The search will be performed by dates.")

    # перевірка на коректність start date
    try:
        start_date = datetime.strptime(start, "%d.%m.%Y")
    except:
        print("Search start date is not specified in the correct format DD.MM.YYYY. Automatic date: 01.01.1970")
        start_date = datetime.strptime("01.01.1970", "%d.%m.%Y")

    # перевірка на коректність end date
    try:
        end_date = datetime.strptime(end, "%d.%m.%Y")
    except:
        print("Search start date is not specified in the correct format DD.MM.YYYY. Automatic date: today")
        end_date = datetime.now()


    with open(f"{Path().cwd()}/note_directory/note.txt", "r+", encoding='utf-8') as file:
        lines = file.readlines()  # список усіх нотаток

    result = "No one note is found."

    # проходимо по кожній нотатці
    for n in lines:

        date = n[:10]  # вирізаємо дату створення нотатки
        date_time = datetime.strptime(date, "%d.%m.%Y")

        if date_time >= start_date and date_time <= end_date:
            # перевірка на keyword
            if (type(keyword) == str) and (keyword != ''):
                if keyword in n.lower():
                    print(n[:len(n)-1])
                    result = "Notes are found."
            else:
                # друкуємо всі строки
                print(n[:len(n)-1])
                result = "Notes are found."

    return result