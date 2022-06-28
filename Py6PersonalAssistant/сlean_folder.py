from Py6PersonalAssistant.clean_folder_tools import file_parser as parser
from Py6PersonalAssistant.clean_folder_tools.normalize import normalize
from pathlib import Path
import shutil

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style

SqlCompleter = WordCompleter(['good bye', 'close', 'exit', '.', 'help', '?', 'parse'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(
        target_folder / (normalize(filename.name)))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(
        target_folder / (normalize(filename.name)))


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / \
                      normalize(filename.name.replace(filename.suffix, ''))

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Обман - это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Не удалось удалить папку {folder}')


def file_parser(*args):
    try:
        folder_for_scan = Path(args[0])
        scan(folder_for_scan.resolve())
    except FileNotFoundError:
        return f"Not able to find '{args[0]}' folder. Please enter a correct folder name."
    except IndexError:
        return "Please enter a folder name."

    for file in parser.JPEG_IMAGES:
        handle_media(file, Path(args[0]) / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, Path(args[0]) / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, Path(args[0]) / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, Path(args[0]) / 'images' / 'SVG')

    for file in parser.AVI_VIDEO:
        handle_media(file, Path(args[0]) / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, Path(args[0]) / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, Path(args[0]) / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, Path(args[0]) / 'video' / 'MKV')

    for file in parser.DOC_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'DOC')
    for file in parser.DOCX_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'DOCX')
    for file in parser.TXT_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'TXT')
    for file in parser.PDF_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'PDF')
    for file in parser.XLSX_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'XLSX')
    for file in parser.PPTX_DOCUMENTS:
        handle_media(file, Path(args[0]) / 'documents' / 'PPTX')

    for file in parser.MP3_AUDIO:
        handle_media(file, Path(args[0]) / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, Path(args[0]) / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, Path(args[0]) / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_media(file, Path(args[0]) / 'audio' / 'AMR')

    for file in parser.ZIP_ARCHIVES:
        handle_archive(file, Path(args[0]) / 'archives')
    for file in parser.GZ_ARCHIVES:
        handle_archive(file, Path(args[0]) / 'archives')
    for file in parser.TAR_ARCHIVES:
        handle_archive(file, Path(args[0]) / 'archives')

    for file in parser.OTHER:
        handle_other(file, Path(args[0]) / 'OTHER')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


def exiting(*args):
    return 'Good bye!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


def helping(*args):
    return """Command format:
        help or ? -> this help;
        parse (folder_name) -> parse files in this folder;
        goodbye or close or exit or . - exit the program"""


COMMANDS = {file_parser: ['parse '], helping: ['?', 'help'], exiting: ['good bye', 'close', 'exit', '.']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def setup_cf():
    print("You are in the clean_folder now. Print 'help' or '?' to get some info about available commands")
    while True:
        user_command = prompt('Enter the command >>> ',
                              history=FileHistory('history'),
                              auto_suggest=AutoSuggestFromHistory(),
                              completer=SqlCompleter,
                              style=style
                              )
        command, data = command_parser(user_command)
        print(command(*data), '\n')
        if command is exiting:
            break


if __name__ == '__main__':
    setup_cf()
