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

import pytest


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


def test_bmi_calc_underweight():
    height, weight = 1.75, 50
    bmi, info_str = bmi_calc(height, weight)
    assert pytest.approx(bmi, abs=1e-2) == 16.33
    assert 'Insufficient body weight' in info_str


def test_bmi_calc_normal():
    height, weight = 1.80, 70
    bmi, info_str = bmi_calc(height, weight)
    assert pytest.approx(bmi, abs=1e-2) == 21.60
    assert 'Normal body weight' in info_str


def test_bmi_calc_overweight():
    height, weight = 1.65, 90
    bmi, info_str = bmi_calc(height, weight)
    assert pytest.approx(bmi, abs=1e-2) == 33.06
    assert 'Excess body weight, watch your figure' in info_str
