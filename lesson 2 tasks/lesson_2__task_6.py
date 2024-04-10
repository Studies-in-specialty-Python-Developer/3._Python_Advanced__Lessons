""" Урок 2, завдання 6
Використовуючи сервіс https://jsonplaceholder.typicode.com/, спробуйте побудувати різні типи
запитів та обробити відповіді. Необхідно попрактикуватися з urllib та бібліотекою requests.
Рекомендується спочатку спробувати виконати запити, використовуючи urllib, а потім спробувати
реалізувати те саме, використовуючи requests.
"""

from urllib import request
import requests
import json

url_response = request.urlopen('https://jsonplaceholder.typicode.com/photos')
url_req_response = request.Request('https://jsonplaceholder.typicode.com/photos')
req_response = requests.get('https://jsonplaceholder.typicode.com/photos')

# Получение различной информации, относящейся к данной странице тремя способами

print(f'--- Status Code\n{url_response.status}\n{""}\n{req_response.status_code}\n')
print(f'--- Headers\n{url_response.getheaders()}\n{url_req_response.headers}\n{req_response.headers}\n')
print(
    f'--- Element of headers\n{url_response.getheader("Content-Type")}\n{""}\n{req_response.headers["Content-Type"]}\n')

url_data = json.loads(url_response.read())
url_req_data = json.loads(request.urlopen(url_req_response).read())
req_data = json.loads(req_response.text)

print(f'---------- Data\n{url_data[0]}\n{url_req_data[0]}\n{req_data[0]}\n')
