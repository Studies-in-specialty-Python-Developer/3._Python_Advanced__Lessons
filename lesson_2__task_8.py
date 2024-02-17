""" Урок 2, завдання 8
Створіть HTTP-клієнта, який прийматиме URL ресурсу, тип методу та словник як передавальні дані
(опціональний). Виконувати запит з отриманим методом на отриманий ресурс, передаючи дані
відповідним методом, та друкувати на консоль статус-код, заголовки та тіло відповіді.
"""

import requests


def get_request(url, method, data=None):
    response = None
    if method.upper() == 'GET':
        response = requests.get(url=url, data=data)
    elif method.upper() == 'POST':
        response = requests.post(url=url, data=data)
    elif method.upper() == 'PUT':
        response = requests.put(url=url, data=data)
    elif method.upper() == 'DELETE':
        response = requests.delete(url=url)
    else:
        print('Wrong method')
    if response is not None:
        print(f'Method: {method}\t')
        print(f'Status Code: {response.status_code}\nURL: {url}')
        print(f'Headers:\n{response.headers}\n')
        print(f'Body\n{response.text}\n')
    return response


params = {
    'q': 'python',
    'type': 'repositories',
}

get_request(r'https://github.com/search?', 'GET', params)
get_request(r'https://github.com/search?', 'POST', params)
get_request(r'https://github.com/search?', 'PUT', params)
get_request(r'https://github.com/search?', 'DELETE')
