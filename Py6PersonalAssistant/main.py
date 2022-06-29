from Py6PersonalAssistant.addressbook import setup_abook
from Py6PersonalAssistant.notes import setup_notes
from Py6PersonalAssistant.сlean_folder import setup_cf

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

SqlCompleter = WordCompleter([
    'addressbook', 'notebook', 'clean folder', 'quit'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})


def main():
    while True:
        print("You are in the menu now. Available commands: 'addressbook', 'notebook', 'clean folder', 'quit'")
        user_command = prompt('Enter the command >>> ',
                                  history=FileHistory('history'),
                                  auto_suggest=AutoSuggestFromHistory(),
                                  completer=SqlCompleter,
                                  style=style
                                  )
        if user_command == "addressbook":
            setup_abook()
        if user_command == "notebook":
            setup_notes()
        if user_command == "clean folder":
            setup_cf()
        if user_command == "quit":
            print('Good bye!')
            break


if __name__ == '__main__':
    main()

