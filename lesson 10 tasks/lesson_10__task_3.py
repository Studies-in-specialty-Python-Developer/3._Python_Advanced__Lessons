""" Урок 10, завдання 3
Витягти всі контактні дані (телефони, пошта, соцмережі тощо) з сайту "https://alfavit.eu/kontakty/".
Дані зберігаються у текстовому файлі.
"""

import re
import requests
from bs4 import BeautifulSoup

contact_templates = [r'\.*Warszawa\.*',  # Adress
                     r'\+\d{2}\s*\d{3}\s*\d{3}\s*\d{3}',  # Phone
                     r'\w+@\w+\.\w+',  # e-mail
                     r'\.*facebook\.*',  # facebook
                     r'\.*instagram\.*',  # instagram
                     ]
response = requests.get('https://alfavit.eu/kontakty/', headers={
    'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})
if response.status_code == 200:
    contact_list = set()
    soup = BeautifulSoup(response.text, 'lxml')
    contact_tags = soup.find_all('span', style='font-size: 14px;')
    for tag in contact_tags:
        for temlate in contact_templates:
            if re.search(temlate, tag.text) is not None:
                contact_list.add(tag.text)
    contact_tags = soup.find_all('a', rel='nofollow')
    for tag in contact_tags:
        for temlate in contact_templates:
            if re.search(temlate, tag.get('href')) is not None:
                contact_list.add(tag.get('href'))
    with open('lesson_8__task_3_alfavit_eu_contacts.txt', 'w', encoding='utf-8') as file:
        for x in contact_list:
            file.write(x + '\n')
else:
    print('Ошибка при получении данных: код', response.status_code)
