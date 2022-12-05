import csv
import re
from prettytable import PrettyTable
import os

dict_of_Names = {'name': 'Название', 'key_skills': 'Навыки',
                    'experience_id': 'Опыт работы',
                    'description': 'Описание',
                    'premium': 'Премиум-вакансия',
                    'salary_from': 'Нижняя граница вилки оклада',
                    'employer_name': 'Компания', 'salary_to': 'Верхняя граница вилки оклада',
                    'salary_gross': 'Оклад указан до вычета налогов',
                    'area_name': 'Название региона', 'salary_currency': 'Идентификатор валюты оклада',
                    'published_at': 'Дата публикации вакансии', 'false': 'Нет',
                    'true': 'Да'}
nameFile = input()

headers_conv = ['Название', 'Описание', 'Навыки', 'Опыт работы',
           'Премиум-вакансия', 'Компания',
           'Оклад', 'Название региона', 'Дата публикации вакансии']

experience_conv = {"moreThan6": "Более 6 лет",
          "between3And6": "От 3 до 6 лет",
          "between1And3": "От 1 года до 3 лет",
          "noExperience": "Нет опыта"}

Empty = True

currency_conv = {"UAH": "Гривны", "EUR": "Евро",
          "AZN": "Манаты",
          "RUR": "Рубли",
          "GEL": "Грузинский лари",
          "KZT": "Тенге",
          "BYR": "Белорусские рубли",
          "KGS": "Киргизский сом",
          "USD": "Доллары",
          "UZS": "Узбекский сум"}


compString = ['Дата публикации вакансии', 'Опыт работы', 'Премиум-вакансия',
              'Название', 'Название региона', 'Компания', 'Описание']


def formatter(item):
    new_row = {}
    salary_inf = []
    count = 0
    for key in item.keys():
        new_line = item[key]
        case_line = item[key]


        if dict_of_Names.__contains__(case_line.lower()): new_line = dict_of_Names[case_line.lower()]
        if key == 'Опыт работы': new_line = experience_conv[case_line.replace(' ', '')]

        if key == 'Дата публикации вакансии':
            new_line = Date_formater(new_line)

        if key in ['Нижняя граница вилки оклада','Оклад указан до вычета налогов', 'Верхняя граница вилки оклада']:
            salary_inf.append(item[key])
            continue
        new_line = Salary_formater(item, key, new_line, salary_inf) if key == 'Идентификатор валюты оклада' else new_line

        new_line = clear_line(new_line)
        if key == 'Навыки':
            l = new_line.split(', ')
            new_line = '\n'.join(l)
        new_row[headers_conv[count]] = new_line
        count += 1
    return new_row


def Date_formater(new_line):
    return f"{new_line[8:10]}.{new_line[5:7]}.{new_line[:4]}"


def Salary_formater(item, ind, text, salary_date):
    salary_date.append(item[ind])
    s_to = salary_date[1]
    s_from = salary_date[0]
    splitter = salary_date[0].find('.')
    splitter_to = salary_date[1].find('.')
    if splitter != -1:
        s_from = salary_date[0][:splitter]
        s_to = salary_date[1][:splitter_to]
    Vichet = dict_of_Names[salary_date[2].lower()] == 'Да'
    if Vichet:
        experience = 'Без вычета налогов'
    else:
        experience = 'С вычетом налогов'
    text = f'{s_from[:-3]} {s_from[-3:]} - {s_to[:-3]} {s_to[-3:]} '
    text += f'({currency_conv[salary_date[3]]}) ({experience})'

    return text


def clear_line(text):
    new_text = re.sub(r"<.*?>", "", text).strip()
    if new_text.find("\n") != -1: new_text = ', '.join(new_text.split('\n'))
    out = re.sub("\s+", " ", new_text)
    return out


def Filt_csv(text, names):
    strings = []
    vacansy = []
    names_amount = len(names)
    Skip_Empty_Strings(names_amount, strings, text)
    for string in strings:
        vacancy_dict = {}
        for i in range(names_amount):
            vacancy_dict[dict_of_Names[names[i]]] = clear_line(string[i])
        vacansy.append(vacancy_dict)
    return vacansy


def Skip_Empty_Strings(names_amount, strings, text):
    for string in text:
        NotEmptyLine = [x for x in string if x != ""]
        if names_amount == len(NotEmptyLine): strings.append(NotEmptyLine)


def Salary_from_data(Sal):
    ful = Sal[:Sal.find('(')].split('-')
    sal_to = ful[1].replace(' ', '')
    sal_from = ful[0].replace(' ', '')
    cur = Sal[Sal.find('(') + 1:Sal.find(')')]
    return (sal_from, sal_to, cur)


def Is_filt_Sal(vac, key, value):
    #преобразование в отдельной фукции
    fromSalary, toSalary, cur = Salary_from_data(vac['Оклад'])
    if key == 'Идентификатор валюты оклада':
        return cur == value
    elif int(fromSalary) <= int(value) <= int(toSalary):
        return True
    return False


def Data_in_Sheet(Data, table, filter):
    global Empty
    index = 1
    for item in Data:
        item = formatter(item)
        if filter(item, Filt_by_key, filt_by_val):

            Empty = False
            row = [index]
            index += 1
            Tablel_Filler(row, table, item)
    return table


def Tablel_Filler(row, table, item):
    for key in item.keys():
        New_row = re.sub("\s+", " ", item[key])
        if key == 'Навыки':
            New_row = New_row.split(', ')
            New_row = '\n'.join(item[key].split(', '))
        if len(New_row) >= 100: New_row = f"{New_row[:100]}..."
        row.append(New_row)
    table.add_row(row)


def filterEmpty(vacancy, key, value):
    return True

def Is_filt_Comp(item, key, row):
    if item[key] == row: return True
    return False

def Is_filt_Cont(item, key, row):
    filer_val = row.split(', ')
    points = item[key].split('\n')
    for row in filer_val:
        if not points.__contains__(row): return False
    return True


def reader_csv(name_file):
    if os.stat(name_file).st_size == 0:
        return [], []
    with open(name_file, encoding='UTF-8-sig') as csvfile:
        read = csv.reader(csvfile)
        header = next(read)
        dic = []
        for item in read:
            if '' not in item \
                    and len(item) == len(header):
                dic.append(item)
        return dic, header


output = ''
Ful_filt = ''
Filt_by_key = ''
filt_by_val = ''

PT_print_start = input().split(' ')
PT_print_end = 0

fields = ['№'] + input().split(', ')
if fields == ['№', '']:
    fields = ['№'] + headers_conv



if len(Ful_filt.split(': ')) == 2:
    filt_by_val = Ful_filt.split(': ')[1]
    Filt_by_key = Ful_filt.split(': ')[0]


Is_filter_function = filterEmpty
if Filt_by_key in ['Оклад', 'Идентификатор валюты оклада']:
    Is_filter_function = Is_filt_Sal
elif Filt_by_key in compString:
    Is_filter_function = Is_filt_Comp
elif Filt_by_key == 'Навыки':
    Is_filter_function = Is_filt_Cont
else: output = 'Параметр поиска некорректен таблицу не печатать'

if Ful_filt.find(':') == -1:
    output += 'Формат ввода некорректен таблицу не печатать'
if Ful_filt == '':
    output = ''

data, header = reader_csv(nameFile)
vacancies_data = Filt_csv(data, header)

March_table = PrettyTable()
March_table.field_names = ['№'] + headers_conv
March_table.max_width = 20
March_table.hrules = True
March_table.align = "l"
March_table = Data_in_Sheet(vacancies_data, March_table, Is_filter_function)


PT_print_end = (int(PT_print_start[1]) - 1) if (len(PT_print_start) == 2 and PT_print_start[0] != 0) else len(vacancies_data)
PT_print_start = (int(PT_print_start[0]) - 1) if PT_print_start[0] != "" else 0



if len(header) == 0:
    output = "Пустой файл"
elif len(data) == 0:
    output = "Нет данных"

if output != '':
    print(output)

else:
    print(March_table.get_string(start=PT_print_start, end=PT_print_end, fields=fields))
