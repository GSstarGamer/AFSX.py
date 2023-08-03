from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from time import sleep as wait
import pydirectinput
from tabulate import tabulate
import shutil
import keyboard
import os
from functions.ssFindnClick import *
from functions.waitForButton import wait as waitForbutton
from functions.waitForButton import clickTillgone
import json
from threading import Thread
import functions.PyUtls as logger
import pytesseract
import platform

config = json.load(open('config.json'))
os_got = platform.system()


screen_width, screen_height = pydirectinput.size()
if os == "Darwin":
    pass
else:
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

middle_x = screen_width // 2
middle_y = screen_height // 2
running = True
work_done = 0
work_done_withoutSpace = 0
sets = 1
types = {
    'Strength': {'key': 1, 'work_done': 0},
    'Durability': {'key': 2, 'work_done': 0},
    'Chakra': {'key': 3, 'work_done': 0},
    'Sword': {'key': 4, 'work_done': 0},
}
typesC = config["types"]
typesC = [typeG.capitalize() for typeG in typesC]


def on_exit():
    global work_done, work_done_withoutSpace
    os.system('cls' if os.name == 'nt' else 'clear')
    endData = [
        ["Strength", "Durability", "Chakra",
         "Sword", "Jumps", "Work Done", "Power"],
        [types['Strength']['work_done'], types['Durability']
         ['work_done'], types['Chakra']['work_done'], types['Sword']['work_done'], work_done-work_done_withoutSpace, work_done, power]
    ]
    print_table(endData)
    logger.log('Exited')
    exit()


def on_key_press(event):
    global running
    if event.name == 'p':
        if running:
            logger.log("paused")
            running = False
        else:
            init(1)
            running = True


keyboard.on_press(on_key_press)


def print_table(data):
    ret = tabulate(data, headers="firstrow", tablefmt="grid")
    print(ret)
    return ret


def get_local_time():
    now = datetime.now()
    time_str = now.strftime("%I:%M %p - %d/%m")
    return time_str


def print_centered_header(header_text, char='=', padding=3):
    terminal_width = shutil.get_terminal_size().columns

    available_width = terminal_width - 2 * padding
    header_text_length = len(header_text)

    if header_text_length >= available_width:
        print(header_text[:available_width])
    else:
        remaining_width = available_width - header_text_length
        half_padding = char * (remaining_width // 2)
        centered_header = f"{half_padding}{header_text}{half_padding}"
        print(centered_header)


def press_key(key):
    pydirectinput.keyDown(str(key))
    pydirectinput.keyUp(str(key))


def autoReconnect():
    if clickTillgone('images/reconnect.png'):
        logger.log('Reconnecting')
        waitForbutton('images/playb.png')
        clickTillgone('images/fastmode.png')
        clickTillgone('images/playb.png')
        logger.success('Reconnected :D')


def startG():
    if clickTillgone('images/fastmode.png'):
        clickTillgone('images/playb.png')
        press_key('tab')
    logger.log('Loaded Game')


def docLog(doc_id, new_content):
    creds = service_account.Credentials.from_service_account_file(
        'docLoggerCred.json')

    service = build('docs', 'v1', credentials=creds)

    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': new_content,
            },
        },
    ]

    service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests},
    ).execute()


def init(sec):
    logger.log('ABOUT TO START, OPEN ROBLOX')
    for i in range(sec):
        down = sec - i
        logger.log(f'STARTING IN {down}')
        wait(1)
    startG()


def work(num_clicks, typeG):
    global work_done_withoutSpace, work_done, running, types
    for i in range(num_clicks):
        if not running:
            return
        down = num_clicks - i
        pydirectinput.click(middle_x, middle_y+50)
        work_done_withoutSpace += 1
        press_key('space')
        work_done += 2
        types[typeG]['work_done'] += 1
        logger.log(f'+1 {typeG}. {down} left')
        wait(.5)


def getDetails():
    x1, y1 = 1658, 458
    x2, y2 = 1754, 482

    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    extracted_text = pytesseract.image_to_string(screenshot)
    extracted_text = extracted_text.replace('\n', '')
    if extracted_text == '' or extracted_text == ' ':
        press_key('tab')
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        extracted_text = pytesseract.image_to_string(screenshot)
        extracted_text = extracted_text.replace('\n', '')
    return extracted_text


try:
    init(5)
    while True:
        if running:
            for typeG, v in types.items():
                if typeG in typesC and running:
                    print_centered_header(f' {typeG} - Set {sets} ')
                    key = v['key']
                    press_key(key)
                    work(config['workPerSet'], typeG)
                    sets += 1
                autoReconnect()
            print_centered_header(' itter Done ')
            power = getDetails().split('/')[0]
            endData = [
                ["Strength", "Durability", "Chakra",
                    "Sword", "Jumps", "Work Done", "Power"],
                [types['Strength']['work_done'], types['Durability']
                    ['work_done'], types['Chakra']['work_done'], types['Sword']['work_done'], work_done-work_done_withoutSpace, work_done, power]
            ]
            logThis = print_table(endData)
            localTime = get_local_time()
            Thread(target=docLog, args=(
                config['docID'], f'\n[{localTime}] Work Done: {work_done}, w/o jump: {work_done_withoutSpace}, Power: {power}', )).start()
except KeyboardInterrupt:
    on_exit()
except Exception as e:
    logger.error(e)
