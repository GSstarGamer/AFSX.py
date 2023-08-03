import requests
import concurrent.futures
from time import sleep as wait

import random
import string


def generate_random_username(length=8):
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_random_credentials(username_length=8, password_length=12):
    username = generate_random_username(username_length)
    password = generate_random_password(password_length)
    return username, password


def send(user, passw):
    headers = {
        'authority': 'my-first-websiet-d.robloxfan123519.repl.co',
        'accept': '*/*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://my-first-websiet-d.robloxfan123519.repl.co',
        'referer': 'https://my-first-websiet-d.robloxfan123519.repl.co/signup',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'u': user,
        'p': passw,
    }

    response = requests.post(
        'https://my-first-websiet-d.robloxfan123519.repl.co/api/signup', headers=headers, json=json_data)
    if response.status_code == 200:
        print('yay: ', user, passw)
    else:
        print(':C')
    return


# with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
#     while True:
#         u, p = generate_random_credentials()
#         future = executor.submit(send, u, p)
