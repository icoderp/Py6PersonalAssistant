from collections import UserDict
from datetime import date
from pathlib import Path
import datetime
import pickle
import re

# --------------------------------Prompt Toolkit-------------------------------
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

SqlCompleter = WordCompleter([
    'hello', 'add ', 'info', 'delete user', 'change phone ', 'show phone', 'delete phone',
    'show all', 'good bye', 'close', 'exit', '.', 'show birthday', 'update birthday',
    'delete birthday', 'birthdays in ', 'show email', 'update email', 'delete email',
    'help', '?', 'search', 'update address', 'delete address'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#884444',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})
# --------------------------------Prompt Toolkit-------------------------------

N = 2 # кількість записів для представлення телефонної книги


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other.value


class Name(Field):
    pass


class Birthday(Field):
    def __str__(self):
        if self.value is None:
            return 'Unknown'
        else:
            return f'{self.value:%d %b %Y}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            try:
                self.__value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError:
                raise DateError


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        def is_code_valid(phone_code: str):
            if '06' in phone_code[:2] or '09' in phone_code[:2] or '05 ' in phone_code[:2]:
                return True
            return False

        valid_phone = None
        phone_num = value.removeprefix('+')
        if phone_num.isdigit():
            if '0' in phone_num[0] and len(phone_num) == 10 and is_code_valid(phone_num[:3]):
                valid_phone = '+38' + phone_num
            if '380' in phone_num[:3] and len(phone_num) == 12 and is_code_valid(phone_num[2:5]):
                valid_phone = '+' + phone_num
        if valid_phone is None:
            raise ValueError(f'Wrong type of {value}')
        self.__value = valid_phone


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            result = None
            valid_emails = re.findall(r'\b[a-zA-Z][\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}', value)
            if valid_emails:
                for i in valid_emails:
                    result = i
            if result is None:
                raise ValueError(f"Wrong type of {value}")
            self.__value = result


class Address(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value


class Record:
    def __init__(self, name: Name, phones=[], birthday=None, email=None, address=None) -> None:
        self.name = name
        self.phone_list = phones
        self.birthday = birthday
        self.email = email
        self.address = address

    def __str__(self) -> str:
        return f'\n|{"-" * 90}|\n' \
               f'| User {self.name!s:<42} Birthday: {self.birthday!s:<15} \n' \
               f'| Email: {self.email!s:<40} Phones: {", ".join([phone.value for phone in self.phone_list])!s:<40} \n' \
               f'| Address: {self.address!s:<60} '\
               f'\n|{"-" * 90}|\n'

    def add_phone(self, phone: Phone) -> None:
        self.phone_list.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phone_list.remove(phone)

    def del_email(self, email: Email) -> None:
        self.email = '-'

    def del_birthday(self, birthday: Birthday) -> None:
        self.birthday = '-'

    def del_address(self, address: Address) -> None:
        self.address = '-'

    def edit_phone(self, phone_num: Phone, new_phone_num: Phone):
        self.phone_list.remove(phone_num)
        self.phone_list.append(new_phone_num)

    def days_to_birthday(self, birthday: Birthday):
        if birthday.value is None:
            return None
        right_now = date.today()
        birthday_day = date(right_now.year, birthday.value.month, birthday.value.day)
        if birthday_day < right_now:
            birthday_day = date(right_now.year + 1, birthday.value.month, birthday.value.day)
        return (birthday_day - right_now).days


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.n = None

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def iterator(self, func=None, days=0):
        index, print_block = 1, ''
        for record in self.data.values():
            if func is None or func(record):
                print_block += str(record)
                if index < N:
                    index += 1
                else:
                    yield print_block
                    index, print_block = 1, ''
        yield print_block


class DateError(Exception):
    ...


class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, contacts, *args):
        try:
            return self.func(contacts, *args)
        except IndexError:
            return 'Error! Give me name and phone please!'
        except KeyError:
            return 'Error! User not found!'
        except ValueError:
            return 'Error! Phone number or email is incorrect!'
        except DateError:
            return 'You cannot add an invalid date'


def hello(*args):
    return 'Hello! Can I help you?'


@InputError
def add(contacts, *args):
    name = Name(args[0])
    if name.value in contacts:
        phone = Phone(args[1])
        contacts[name.value].add_phone(phone)
        writing_file(contacts)
        return f'Add phone {phone} to user {name}'
    else:
        phone = Phone(args[1])
        birthday = '-'
        email = '-'
        address = '-'
        if len(args) > 2:
            birthday = Birthday(args[2])
        if len(args) > 3:
            email = Email(args[3])
        if len(args) > 4:
            address = Address(" ".join(args[4:]))
        contacts[name.value] = Record(name, [phone], birthday, email, address)
        writing_file(contacts)
        return f'Add user {name} with phone number {phone}, birthday {birthday}, email {email}, address {address}'


@InputError
def del_user(contacts, *args):
    name = args[0]
    del contacts[name]
    writing_file(contacts)
    return f'Deleted user {name}'


@InputError
def change(contacts, *args):
    name, old_phone, new_phone = args[0], args[1], args[2]
    contacts[name].edit_phone(Phone(old_phone), Phone(new_phone))
    writing_file(contacts)
    return f'Change to user {name} phone number from {old_phone} to {new_phone}'


@InputError
def phone(contacts, *args):
    if args:
        name = args[0]
        res = ''
        for el in contacts[name].phone_list:
            res += f'{el}\n'
        return res


@InputError
def info(contacts, *args):
    if args:
        name = args[0]
        return contacts[name]


@InputError
def del_phone(contacts, *args):
    name, phone = args[0], args[1]
    contacts[name].del_phone(Phone(phone))
    writing_file(contacts)
    return f'Delete phone {phone} from user {name}'


def show_all(contacts, *args):
    if not contacts:
        return 'Address book is empty'
    result = 'List of all users:\n'
    print_list = contacts.iterator()
    for item in print_list:
        result += f'{item}'
    return result


@InputError
def email(contacts, *args):
    if args:
        name = args[0]
        return f'{contacts[name].email}'


@InputError
def add_email(contacts, *args):
    name, email = args[0], args[1]
    contacts[name].email = Email(email)
    writing_file(contacts)
    return f'Email {contacts[name].email} of {name} was added or changed'


@InputError
def del_email(contacts, *args):
    name, email = args[0], args[1]
    contacts[name].del_email(Email(email))
    writing_file(contacts)
    return f'Delete email {email} from user {name}'


@InputError
def birthday(contacts, *args):
    if args:
        name = args[0]
        return f'{contacts[name].birthday}'


@InputError
def add_update_date(contacts, *args):
    name, birthday = args[0], args[1]
    contacts[name].birthday = Birthday(birthday)
    writing_file(contacts)
    return f'Birthday date {contacts[name].birthday} of {name} was added or changed'


@InputError
def del_birthday(contacts, *args):
    name, birthday = args[0], args[1]
    contacts[name].del_birthday(Birthday(birthday))
    writing_file(contacts)
    return f'Delete birthday {birthday} from user {name}'


def show_birthday_n_days(contacts, *args):
    def func_days(record):
        return record.birthday.value is not None and record.days_to_birthday(record.birthday) <= days

    days = int(args[0])
    result = f'List of users with birthday in {days} days:\n'
    print_list = contacts.iterator(func_days)
    for item in print_list:
        result += f'{item}'
    return result


@InputError
def address(contacts, *args):
    if args:
        name = args[0]
        return f'{contacts[name].address}'


@InputError
def add_address(contacts, *args):
    name, address = args[0], " ".join(args[1:])
    contacts[name].address = Address(address)
    writing_file(contacts)
    return f'Address {contacts[name].address} of {name} was added or changed'


@InputError
def del_address(contacts, *args):
    name, address = args[0], " ".join(args[1:])
    contacts[name].del_address(Address(address))
    writing_file(contacts)
    return f'Delete address {address} from user {name}'


def exiting(*args):
    return 'Good bye!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


def helping(*args):
    return """Command format:
        help or ? -> this help;
        hello -> greeting;
        add (name) (phone) (birthday) (email) (address) -> 1st use: add user to directory, 2nd use: add 1 more phone number;
        info (name) -> all information about user;
        delete user (name) -> delete user from address book;
        change phone (name) (old_phone) (new_phone) -> change the user's phone number;
        show phone (name) -> show all user`s phones;
        delete phone (name) (phone) -> delete the user's phone number;
        show all -> show data of all users;
        show birthday (name) -> show user`s birthday;
        update birthday (name) (birthday) -> add/update user`s birthday;
        delete birthday (name) (birthday) -> delete user`s birthday;
        birthdays in (number) -> show users with birthday in number days;
        show email (name) -> show user`s email;
        update email (name) (email) -> add/update user`s email;
        delete email (name) (email) -> delete user`s email;
        show address (name) -> show user`s address;
        update address (name) (address) -> add/update user`s address;
        delete address (name) (address) -> delete user`s address;
        search -> show users with matches for you request (WARNING! All user`s info should be filled,
        'None' fields will cause error);
        goodbye or close or exit or . - exit the program"""


file_name = 'AddressBook.bin'


def reading_file(file_name):
    with open(file_name, "rb") as file:
        try:
            unpacked = pickle.load(file)
        except EOFError:
            unpacked = AddressBook()
        return unpacked


def writing_file(contacts):
    with open(file_name, "wb") as file:
        pickle.dump(contacts, file)


@InputError
def find(contacts, *args):
    def find_sub(record):
        try:
            return subst.lower() in record.name.value.lower() or \
                   any(subst in phone.value for phone in record.phone_list) or \
                   (record.birthday.value is not None and subst in record.birthday.value.strftime('%d.%m.%Y')) or \
                   (record.email.value is not None and subst in record.email.value) or \
                   (record.address.value is not None and subst in record.address.value)
        except AttributeError:
            return False

    subst = args[0]
    res = f'List of users with \'{subst.lower()}\' in data:\n'
    page = contacts.iterator(find_sub)
    for el in page:
        res += f'{el}'
    return res


def start_file():  # перевірка чи файл 'AddressBook.bin' створений

    global file
    try:
        file = open(f"{Path().cwd()}/{file_name}", 'rb')
        print(f"File {file_name} is loaded.")
    except:
        file = open(f"{Path().cwd()}/{file_name}", 'wb')
        print(f"File {file_name} is created.")
    finally:
        file.close()


COMMANDS = {hello: ['hello'], add: ['add '], info: ['info'], del_user: ['delete user'], change: ['change phone '],
            phone: ['show phone'], del_phone: ['delete phone'], show_all: ['show all'],
            exiting: ['good bye', 'close', 'exit', '.'], birthday: ['show birthday'],
            add_update_date: ['update birthday'], del_birthday: ['delete birthday'],
            show_birthday_n_days: ['birthdays in '], email: ['show email'], add_email: ['update email'],
            del_email: ['delete email'], address: ['show address'], add_address: ['update address'],
            del_address: ['delete address'], helping: ['help', '?'], find: ['search']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def setup_abook():
    start_file()
    contacts = reading_file(file_name)
    print("You are in the addressbook now. Print 'help' or '?' to get some info about available commands")
    while True:
        user_command = prompt('Enter the command >>> ',
                              history=FileHistory('addressbook_history'),
                              auto_suggest=AutoSuggestFromHistory(),
                              completer=SqlCompleter,
                              style=style
                              )
        command, data = command_parser(user_command)
        print(command(contacts, *data))
        if command is exiting:
            break


if __name__ == '__main__':
    setup_abook()