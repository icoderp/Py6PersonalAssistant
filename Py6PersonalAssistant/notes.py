from datetime import datetime
from pathlib import Path

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

SqlCompleter = WordCompleter([
    'add ', 'search ', 'find ', 'show all', 'change ',
    'del ', 'tag ', 'good bye', 'close', 'exit', '.', 'help', '?'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})


to_check = 'show all'


def start_note():  # перевірка чи файл "note.txt" створений

    try:
        file = open(f"{Path().cwd()}/note.txt", 'r')
        print("File note.txt with notes is loaded.")
    except:
        file = open(f"{Path().cwd()}/note.txt", 'w')
        print("File note.txt with notes is created.")
    finally:
        file.close()


def add_note(*args):
    """
    Зберігає нотатку за шляхом .\note_directory\note.txt в note.txt
    формат запису: DD.MM.YYYY - hh.mm.ss | Note
    """
    note = ' '.join(args)
    date_now = datetime.now()
    str_date_now = date_now.strftime("%d.%m.%Y - %H:%M:%S")
    with open(f"{Path().cwd()}/note.txt", "a+", encoding='utf-8') as file:
        file.write(f'{str_date_now} | {note}\n')

    return "The note is added."


def find_note(*args):
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
        if to_check == 'show all':
            print('All notes')
        else:
            print("Keyword not specified. The search will be performed by dates.")

    # перевірка на коректність start date
    try:
        start_date = datetime.strptime(start, "%d.%m.%Y")
    except:
        if to_check != 'show all':
            print("Search start date is not specified in the correct format DD.MM.YYYY. Automatic date: 01.01.1970")
        start_date = datetime.strptime("01.01.1970", "%d.%m.%Y")

    # перевірка на коректність end date
    try:
        end_date = datetime.strptime(end, "%d.%m.%Y")
    except:
        if to_check != 'show all':
            print("Search start date is not specified in the correct format DD.MM.YYYY. Automatic date: today")
        end_date = datetime.now()

    with open(f"{Path().cwd()}/note.txt", "r+", encoding='utf-8') as file:
        lines = file.readlines()  # список усіх нотаток

    result = "No one note is found."

    # проходимо по кожній нотатці
    for n in lines:

        date = n[:10]  # вирізаємо дату створення нотатки
        date_time = datetime.strptime(date, "%d.%m.%Y")

        if (date_time >= start_date) and (date_time <= end_date):
            # перевірка на keyword
            if (type(keyword) == str) and (keyword != ''):
                if keyword in n.lower():
                    print(n[:len(n) - 1])
                    result = "Notes are found."
            else:
                # друкуємо всі строки
                print(n[:len(n) - 1])
                result = "Notes are found."

    return result


def change_note(*args):
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
            with open(f"{Path().cwd()}/note.txt", "r") as file:
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
            with open(f"{Path().cwd()}/note.txt", "w") as file:
                file.writelines(lines)

        except:
            print("Notepad error, check it.")

    except:
        print("Incorrect format: DD.MM.YYYY - hh.mm.ss. Copy the date and time from the search results.")

    return result


def delete_note(*args):
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
            with open(f"{Path().cwd()}/note.txt", "r") as file:
                lines = file.readlines()
            for n in range(len(lines)):
                date = lines[n][:21]  # ціла дата DD.MM.YYYY - hh.mm.ss
                date_s = datetime.strptime(date, "%d.%m.%Y - %H:%M:%S")
                if date_s == date_str:  # збіг дати і часу строки з заданою датою і часом
                    lines.pop(n)
                    result = "The note is deleted"
                    break
            # видаляємо вміст старого файлу, пишемо змінений
            with open(f"{Path().cwd()}/note.txt", "w") as file:
                file.writelines(lines)

        except:
            print("Notepad error, check it.")

    except:
        print("Incorrect format: DD.MM.YYYY - hh.mm.ss. Copy the date and time from the search results.")

    return result


def tag_note(*args):
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
            with open(f"{Path().cwd()}/note.txt", "r") as file:
                lines = file.readlines()
            for n in range(len(lines)):
                date = lines[n][:21]  # ціла дата DD.MM.YYYY - hh.mm.ss
                date_s = datetime.strptime(date, "%d.%m.%Y - %H:%M:%S")
                if date_s == date_str:  # збіг дати і часу строки з заданою датою і часом
                    if tag != '':
                        new_line = f"{lines[n][:len(lines[n]) - 1]} {tag}\n"  # добавлення тегу в вибрану нотатку
                        lines[n] = new_line
                        result = "The hashtag is accepted."
                        break
                    else:
                        user_answer = input("The tag is empty. Are you sure? y or n")
                        if user_answer == 'y':
                            new_line = f"{lines[n][:len(lines[n]) - 1]} {tag}\n"
                            lines[n] = new_line
                            result = "The hashtag is accepted."
                        break
            # видаляємо вміст старого файлу, пишемо змінений
            with open(f"{Path().cwd()}/note.txt", "w") as file:
                file.writelines(lines)
        except:
            print("Notepad error, check it.")

    except:
        print("Incorrect format: DD.MM.YYYY - hh.mm.ss. Copy the date and time from the search results.")

    return result


def helping(*args):
    return """
        Command format:
        help or ? -> this help;
        add -> add a note 
            | Ex. add The weather is good today
        search or find -> Search by keyword in notes 
            | Ex. find today 
            | Ex. find today 01.01.2022 07.01.2022 
        change -> Changes the note 
            | Ex. change 01.01.2022 Happy New Year
        tag -> adds a tag to a note
            | Ex. tag 01.01.2022 - 00:11:34 #happy
        del -> deletes the note
            | Ex. del 01.01.2022 - 00:11:34
        show all -> show all notes
        goodbye or close or exit or . -> exit the notes
        """


def unknown_command(*args):
    return 'Unknown command! Enter again!'


def exiting(*args):
    return 'Good bye!'


COMMANDS = {add_note: ['add '], find_note: ['search ', 'find ', 'show all'],
            change_note: ['change '], delete_note: ['del '], tag_note: ['tag '],
            exiting: ['good bye', 'close', 'exit', '.'], helping: ['help', '?']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def setup_notes():
    print("You are in the notes now. Print 'help' or '?' to get some info about available commands")
    start_note()
    while True:
        user_command = prompt('Enter the command >>> ',
                              history=FileHistory('notes_history'),
                              auto_suggest=AutoSuggestFromHistory(),
                              completer=SqlCompleter,
                              style=style
                              )
        command, data = command_parser(user_command)
        print(command(*data))
        if command is exiting:
            break


if __name__ == '__main__':
    setup_notes()
