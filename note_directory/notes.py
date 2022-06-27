import pickle
from datetime import datetime
from pathlib import Path

from main import AddressBook


def add_note(contacts, *args):
    """
    Зберігає нотатку за шляхом .\note_directory\note.txt в note.txt
    формат запису: DD.MM.YYYY - hh.mm.ss | Note
    """
    note = ' '.join(args)
    date_now = datetime.now()
    str_date_now = date_now.strftime("%d.%m.%Y - %H:%M:%S")
    with open(f"{Path().cwd()}/note_directory/note.txt", "a+", encoding='utf-8') as file:
        file.write(f'{str_date_now} | {note}\n')

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


def change_note(contacts, *args):
    """
    Щоб змінити нотатку потрібно вказати дату і час її створення і вказати нову
    дату і час можна дізнатися за допомогою функції find_note
    пр. change note 20.02.1991 - 14:28:06 print("Hello world!")
    """
    # розбираємо аргументи в форматі: datetime_line: "%d.%m.%Y - %H:%M:%S" = '', text: str = ''
    if len(args) >= 4:
        datetime_line = f"{args[0]} {args[1]} {args[2]}"
        args = args[3:]
        text = ' '.join(args)
    elif len(args) == 3:
        datetime_line = args[0] + args[1] + args[2]
        text = ''
    else:
        datetime_line = ''
        text = ''

    result = "No one note is changed."
    try:
        # перевірка, що ідентифікатор заданий у правильному форматі
        date_str = datetime.strptime(datetime_line, "%d.%m.%Y - %H:%M:%S")
        try:
            with open(f"{Path().cwd()}/note_directory/note.txt", "r") as file:
                lines = file.readlines()
            for n in range(len(lines)):
                date = lines[n][:21]  # ціла дата DD.MM.YYYY - hh.mm.ss
                n_id = datetime.strptime(date, "%d.%m.%Y - %H:%M:%S")
                if n_id == date_str:  # збіг дати і часу строки з заданою датою і часом
                    if text != '':
                        # заміна строки, дата і час не міняється
                        lines[n] = f"{date} | {text}\n"
                        result = "The note is changed"
                        break
                    else:
                        user_answer = input("The field for change is empty. Are you sure? y or n")
                        if user_answer == 'y':
                            # заміна строки, дата і час не міняється
                            lines[n] = f"{date} | {text}\n"
                            result = "The note is changed"
                        break
            # видаляємо вміст старого файлу, пишемо змінений
            with open(f"{Path().cwd()}/note_directory/note.txt", "w") as file:
                file.writelines(lines)
                
        except:
            print("Notepad error, check it.")

    except:
        print("Incorrect format: DD.MM.YYYY - hh.mm.ss. Copy the date and time from the search results.")

    return result


def delete_note(contacts, *args):
    """
    Щоб видалити нотатку потрібно вказати дату і час її створення
    дату і час можна дізнатися за допомогою функції find_note
    пр. del note 20.02.1991 - 14:28:06
    """
    # розбираємо аргументи в форматі: datetime_line: "%d.%m.%Y - %H:%M:%S" = '', text: str = ''
    if len(args) == 3:
        datetime_line = f"{args[0]} {args[1]} {args[2]}"
    else:
        datetime_line = ''

    result = "No one note is deleted"
    try:
        # перевірка, що ідентифікатор заданий у правильному форматі
        date_str = datetime.strptime(datetime_line, "%d.%m.%Y - %H:%M:%S")
        try:
            with open(f"{Path().cwd()}/note_directory/note.txt", "r") as file:
                lines = file.readlines()
            for n in range(len(lines)):
                date = lines[n][:21]  # ціла дата DD.MM.YYYY - hh.mm.ss
                date_s = datetime.strptime(date, "%d.%m.%Y - %H:%M:%S")
                if date_s == date_str:  # збіг дати і часу строки з заданою датою і часом
                    lines.pop(n)
                    result = "The note is deleted"
                    break
            # видаляємо вміст старого файлу, пишемо змінений
            with open(f"{Path().cwd()}/note_directory/note.txt", "w") as file:
                file.writelines(lines)

        except:
            print("Notepad error, check it.")

    except:
        print("Incorrect format: DD.MM.YYYY - hh.mm.ss. Copy the date and time from the search results.")

    return result


def tag_note(contacts, *args):
    """
    Додавання тега (#) до нотатки. Нотатка ідентифікується, по даті і часі,
     який можна взнати при пошуку потрібної нотатки
    Пошук по тегам проходить через функцію find_note
    пр. find note #plan
    Приклад додавання тегу: tag note 20.02.1991 - 14:28:06 #plan
    """
    # розбираємо аргументи в форматі: datetime_line: "%d.%m.%Y - %H:%M:%S" = '', text: str = ''
    if len(args) >= 4:
        datetime_line = f"{args[0]} {args[1]} {args[2]}"
        tag = args[3]
    elif len(args) == 3:
        datetime_line = args[0] + args[1] + args[2]
        tag = ''
    else:
        datetime_line = ''
        tag = ''

    result = "The hashtag is not acceptable."
    try:
        # перевірка, що ідентифікатор заданий у правильному форматі
        date_str = datetime.strptime(datetime_line, "%d.%m.%Y - %H:%M:%S")
        try:
            with open(f"{Path().cwd()}/note_directory/note.txt", "r") as file:
                lines = file.readlines()
            for n in range(len(lines)):
                date = lines[n][:21]  # ціла дата DD.MM.YYYY - hh.mm.ss
                date_s = datetime.strptime(date, "%d.%m.%Y - %H:%M:%S")
                if date_s == date_str:  # збіг дати і часу строки з заданою датою і часом
                    if tag != '':
                        new_line = f"{lines[n][:len(lines[n])-1]}  #{tag}\n"  # добавлення тегу в вибрану нотатку
                        lines[n] = new_line
                        result = "The hashtag is accepted."
                        break
                    else:
                        user_answer = input("The tag is empty. Are you sure? y or n")
                        if user_answer == 'y':
                            new_line = f"{lines[n][:len(lines[n]) - 1]}  #{tag}\n"
                            lines[n] = new_line
                            result = "The hashtag is accepted."
                        break
            # видаляємо вміст старого файлу, пишемо змінений
            with open(f"{Path().cwd()}/note_directory/note.txt", "w") as file:
                file.writelines(lines)
        except:
            print("Notepad error, check it.")

    except:
        print("Incorrect format: DD.MM.YYYY - hh.mm.ss. Copy the date and time from the search results.")

    return result


def unknown_command(*args):
    return 'Unknown command! Enter again!'


def exiting(*args):
    return 'Good bye!'


file_name = 'AddressBook.bin'


def reading_file(file_name):
    with open(file_name, "rb") as file:
        try:
            unpacked = pickle.load(file)
        except EOFError:
            unpacked = AddressBook()
        return unpacked


COMMANDS = {add_note: ['add note '], find_note: ['search note', 'find note'],
            change_note: ['change note'], delete_note: ['del note'], tag_note: ['tag note'],
            exiting: ['good bye', 'close', 'exit', '.']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def main():
    contacts = reading_file(file_name)
    while True:
        user_command = input('Enter the command >>> ')
        command, data = command_parser(user_command)
        print(command(contacts, *data))
        if command is exiting:
            break


if __name__ == '__main__':
    main()