""" Урок 10, завдання 2
Витягти телефони із сайту «https://www.miraton.ua/». Дані зберігаються у текстовому файлі.
"""

import re
import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.miraton.ua/', headers={
    'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})
if response.status_code == 200:
    phone_list = set()
    soup = BeautifulSoup(response.text, 'lxml')
    phones = soup.find_all(href=re.compile('tel:'))
    for phone in phones:
        new_phone = str(phone)[len('<a href="tel:'):-str(phone).rfind('">') + 2:]
        if len(new_phone) == 10:
            phone_list.add(f'+38{new_phone}')
        if len(new_phone) == 12:
            phone_list.add(f'+{new_phone}')
    with open('lesson_8__task_2_miraton_phones.txt', 'w', encoding='utf-8') as file:
        for x in phone_list:
            file.write(x + '\n')
else:
    print('Ошибка при получении данных: код', response.status_code)
