""" Урок 3, завдання 2
Створіть XML-файл із вкладеними елементами та скористайтеся мовою пошуку XPATH. Спробуйте
здійснити пошук вмісту за створеним документом XML, ускладнюючи свої запити та додаючи нові
елементи, якщо буде потрібно.
"""

from xml.etree import ElementTree as Et

tree = Et.parse('lesson_3__task_2_example.xml')
root = tree.getroot()

for country in root:
    # Вывод аттрибутов различными способами
    print(country.attrib)
    print("name:", country.get('name'))
    for attr, value in country.attrib.items():
        print(f'{attr}: {value}')
    # Вывод дочерних узлов
    for child in country:
        print('{}: {}'.format(child.tag, child.text))
    print()

for country in root:
    print(country.attrib)
    print('year: {}, gdppc: {}'.format(
        country.find('./year').text,
        country.find('./gdppc').text,
    ))
print()

countries = root.findall('./')
years = root.findall('./country/year')
gdppc_s = root.findall('./country/gdppc')
for values in zip(countries, years, gdppc_s):
    row = {value.tag: value.get('name') if value.tag == 'country' else value.text for value in values}
    print(row)
print()

for country in root:
    print("name: ", country.attrib)
    for child in country:
        print('{}: {}'.format(child.tag, child.text))
print()

gdp = root.find('./country/year/..[@name][1]/gdppc').text
print(gdp)

gdp = root.find('./country/year/..[2]/gdppc').text
print(gdp)

gdp = root.find('./country/gdppc/..[3]/gdppc').text
print(gdp)

gdp = root.find('./country/year/..[@size]/year').text
print(gdp)
