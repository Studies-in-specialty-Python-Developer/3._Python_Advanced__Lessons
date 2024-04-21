""" Урок 10, завдання 1
Створити програму-парсер, яка за допомогою методу get отримує дані зі сторінки
https://ua.onlinemschool.com/math/formula/bradis_table/.
Зчитати дані 1) sin, cos 2) tg, ctg. Зберегти дані у файл формату СSV.
"""

import csv
import requests
from bs4 import BeautifulSoup

response = requests.get('https://ua.onlinemschool.com/math/formula/bradis_table/')
if response.status_code == 200:
    csv_table = []
    csv_row = []
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table', attrs={'border': 1})
    for number, table in enumerate(tables):
        csv_table.clear()
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            csv_row.clear()
            for col in cols:
                csv_cell = str(col).replace('<b>', '').replace('</b>', '').replace('<td>', '').replace('</td>',
                                                                                                       '').strip()
                if '<td colspan="' in csv_cell:
                    colspan = csv_cell.replace('<td colspan="', '')
                    for _ in range(int(colspan[:colspan.find('"')])):
                        csv_row.append('')
                else:
                    csv_row.append(csv_cell)
            if ''.join(csv_row):
                csv_table.append(csv_row[:])
        prefix = 'tg_gtg' if number else 'sin_cos'
        with open(f'lesson_8__task_1_{prefix}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(csv_table)
else:
    print('Ошибка при получении данных: код', response.status_code)
