""" Урок 9, завдання 2
Взяти функцію розрахунку маси тіла з Python Starter українською/Домашнє_завдання 8/Завдання 5. Покрити її 10 тестами,
щоб перевірити роботоздатність, використовуючи заздалегідь валідні дані та навпаки(введення текстових даних у поля,
від'ємні значення тощо).
За необхідності взяти її та доопрацювати до максимально стабільного варіанту.
В процессі тестування використати:
- оператор assert;
- pytest;
- unittest.
"""


def bmi_calc(height, weight):
    bmi = weight / (height ** 2)
    info_str = f'Your BMI is {bmi:.2f}\n'
    if bmi < 18.5:
        info_str += 'Insufficient body weight'
    elif bmi < 25:
        info_str += 'Normal body weight'
    else:
        info_str += 'Excess body weight, watch your figure'
    return bmi, info_str


assert round(bmi_calc(1.8, 80)[0], 2) == 24.69, 'Calculation Error'
assert bmi_calc(-1.8, 80)[0] > 0, 'bmi < 0'
assert round(bmi_calc('1.8', 80)[0], 2) == 24.69, 'Incorrect type of argument'
