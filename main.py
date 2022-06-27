from addressbook import setup_abook
from notes import setup_notes

if __name__ == '__main__':
    while True:
        print("You are in the menu now. Available commands: 'addressbook', 'notebook', 'quit'")
        user_command = input('Enter the command >>> ')
        if user_command == "addressbook":
            setup_abook()
        if user_command == "notebook":
            setup_notes()
        if user_command == "quit":
            print('Good bye!')
            break
