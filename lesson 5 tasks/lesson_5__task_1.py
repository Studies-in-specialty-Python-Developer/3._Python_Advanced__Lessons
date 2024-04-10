""" Урок 5, завдання 1
Створіть співпрограму, яка отримує контент із зазначених посилань і логує хід виконання в спеціальний
файл, використовуючи стандартну бібліотеку urllib, а потім проробіть те саме з бібліотекою aiohttp. Кроки,
які мають бути залоговані: початок запиту до адреси X, відповідь для адреси X отримано зі статусом 200.
Перевірте хід виконання програми на > 3 ресурсах і перегляньте послідовність запису логів в обох
варіантах і порівняйте результати. Для двох видів завдань використовуйте різні файли для логування,
щоби порівняти отриманий результат.
"""

import asyncio
import time
import aiohttp
import urllib.request
import csv

resources = [
    'https://www.python.org/',
    'https://www.google.com.ua/',
    'https://www.microsoft.com/',
    'https://www.wikipedia.org/',
    'https://www.sqlite.org/index.html',
]


def time_format(start_time, end_time):
    """ Report line formatting """
    start_time_format = time.strftime('%M:%S',
                                      time.localtime(start_time)) + f'.{int((start_time - int(start_time)) * 1e6):06d}'
    end_time_format = time.strftime('%M:%S',
                                    time.localtime(end_time)) + f'.{int((end_time - int(end_time)) * 1e6):06d}'
    time_delta = end_time - start_time
    time_delta_format = time.strftime('%S',
                                      time.localtime(time_delta)) + f'.{int((time_delta - int(time_delta)) * 1e6):06d}'
    return start_time_format, end_time_format, time_delta_format


def sync_fetch_url(url):
    """ Sequential resource polling """
    start_time = time.time()
    with urllib.request.urlopen(url, timeout=10) as response:
        print(response.status, url)
    end_time = time.time()
    return response.status, *time_format(start_time, end_time), url


async def async_fetch_url(url):
    """ Asynchronous resource request """
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        async with session.get(url) as response:
            await response.read()
            print(response.status, url)
        end_time = time.time()
        return response.status, *time_format(start_time, end_time), url


async def async_polling(resources_):
    """ Asynchronous resource polling """
    timing_ = []
    for url in resources_:
        timing_.append(await async_fetch_url(url))
    time.sleep(1)
    return timing_


print('   Sequential request')
timing = []
for url_ in resources:
    timing.append(sync_fetch_url(url_))

with open('lesson_5__task_1_sync.log', 'w', newline='') as file:
    fieldnames = ['status', 'start', 'end', 'delta', 'URL']
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(fieldnames)
    for row in timing:
        writer.writerow(row)

print('   Asynchronous request')
timing.clear()

timing = asyncio.run(async_polling(resources))

with open('lesson_5__task_1_async.log', 'w', newline='') as file:
    fieldnames = ['status', 'start', 'end', 'delta', 'URL']
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(fieldnames)
    for row in timing:
        writer.writerow(row)
