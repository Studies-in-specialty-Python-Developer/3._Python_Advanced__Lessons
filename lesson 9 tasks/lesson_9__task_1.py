""" Урок 9, завдання 1
Створити функцію, яка допоможе порахувати швидкість автомобіля. Набір даних, який використовується для розрахунку:
* довжина шляху;
* тривалість шляху.
Створити 5-7 тестів використовуючи оператор assert.
"""

from datetime import datetime


def speed(distance: float, time_str: str) -> float:
    """ Вычисляет скорость автомобиля по пройденной дистанции и затраченному времени
    Arguments:
        distance: дистанция, км
        time_str: затраченное время, ч.
    Returns:
        скорость автомобиля, км/ч """
    time_obj = datetime.strptime(time_str, '%H:%M:%S')
    return distance / (time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600)


distance = 120.0
time = '12:00:00'

assert isinstance(distance, float), 'Incorrect distance type'

assert distance > 0, 'Incorrect distance value'

time_parts = time.split(':')

assert len(time_parts) == 3, 'Incorrect time format'

for part in time_parts:
    assert part.isdigit(), 'Incorrect time value'

assert speed(120, '12:00:00') == 10.0, 'Calculation error'

assert speed(120, '12:00:00') == 0.0, 'Should be 10.0'
