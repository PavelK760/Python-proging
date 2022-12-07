import os
from prettytable import PrettyTable
import csv
import re


def sort_vacancies(data, SortParametre, sort_reserved):
    if SortParametre == "Оклад":
        parametre = lambda x: (float(x["Нижняя граница вилки оклада"]) * currency_to_rub[
            x["Идентификатор валюты оклада"]]) \
                              + (float(x["Нижняя граница вилки оклада"]) * currency_to_rub[
            x["Идентификатор валюты оклада"]]) / 2
    elif SortParametre == "Опыт работы":
        parametre = lambda x: sign_of_exp[x["Опыт работы"]]
    elif SortParametre == "Навыки":
        parametre = lambda x: len(x["Навыки"].split("\n"))
    else:
        parametre = lambda x: x[SortParametre]

    out = sorted(data, key=parametre, reverse=sort_reserved)
    return out


def time_to_format(time):
    return f"{time[8:10]}.{time[5:7]}.{time[:4]}"


def parametre_check(filt_parametre):
    doublepoint_ind = filt_parametre.find(': ')
    answer = None
    impact = None
    if doublepoint_ind == (-1):
        answer = "Формат ввода некорректен"
    else:
        impact = (filt_parametre[:doublepoint_ind], filt_parametre[doublepoint_ind + 2:])
        if impact[0] not in ["Идентификатор валюты оклада"] + layer_of_names:
            impact = None
            answer = "Параметр поиска некорректен"

    return impact, answer


def money_to_format(salary):
    if '.' in salary:
        deleted_point = salary[:salary.find('.')]
    else:
        deleted_point = salary

    if len(deleted_point) > 3:
        first_space = deleted_point[:len(deleted_point) - 3]
    else:
        first_space = ''

    if len(first_space) > 3:
        second_spase = first_space[:len(first_space) - 3]
    else:
        second_spase = ''

    units = deleted_point[len(first_space):]
    thousands = first_space[len(second_spase):]
    millions = second_spase

    if millions:
        return f"{millions} {thousands} {units}"
    elif thousands:
        return f"{thousands} {units}"
    else:
        return units


def string_to_FormatStr(text):
    new_text = clean_from_tags(text)
    # Этот блок нужен для всех пунктов

    new_text = Key_skills_to_FormatStr(new_text)
    # А этот для навыков

    if new_text in dictionary_translator.keys():
        out = dictionary_translator[new_text]
    else:
        out = new_text
    return out


def SortParametre_check(SortParametre):
    if SortParametre not in layer_of_names:
        answer = None
        impact = "Параметр сортировки некорректен"
    else:
        answer = SortParametre
        impact = None
    return answer, impact


def RightRow(layer):
    if layer.pop("Оклад указан до вычета налогов") == "Нет":
        taxes = "С вычетом налогов"
    else:
        taxes = "Без вычета налогов"

    valute = layer.pop("Идентификатор валюты оклада")
    bottom = money_to_format(layer.pop("Верхняя граница вилки оклада"))
    upper = money_to_format(layer.pop("Нижняя граница вилки оклада"))

    salary_result = upper + ' - ' + bottom + f" ({valute}) ({taxes})"
    layer["Оклад"] = salary_result

    layer["Дата публикации вакансии"] = time_to_format(layer["Дата публикации вакансии"])
    return layer


def table_print(data, range_of_rows, names_of_columns, impact, SortParametre, sort_reserved): #CSV_File_Start
    pretty_table = PrettyTable()
    pretty_table.hrules = True
    pretty_table.align = 'l'
    pretty_table.field_names = layer_of_names
    pretty_table.max_width = 20

    if impact:
        data = select_by_parametre(data, impact)
        if len(data) == 0:
            return print("Ничего не найдено")

    if impact and SortParametre:
        data = select_by_parametre(data, impact)

        if len(data) != 0:
            if SortParametre:
                data = sort_vacancies(data, SortParametre, sort_reserved)
            table_filler(data, pretty_table)
        else:
            print("Ничего не найдено")
            return
    else:
        if SortParametre:
            data = sort_vacancies(data, SortParametre, sort_reserved)
        table_filler(data, pretty_table)

    t = pretty_table[slice(*(range_of_rows + [None]))]
    if names_of_columns:
        Fields = ["№"] + names_of_columns
    else:
        Fields = []
    print_table = t.get_string(fields=Fields)
    print(print_table)


def select_by_parametre(data, impact):
    result_list = []
    if impact[0] == "Дата публикации вакансии":
        for item in data:
            if time_to_format(item[impact[0]]) == impact[1]:
                result_list.append(item)
    elif impact[0] == "Оклад":
        for item in data:
            if float(item["Нижняя граница вилки оклада"]) <= float(impact[1]) <= float(
                    item["Верхняя граница вилки оклада"]):
                result_list.append(item)
    elif impact[0] == "Навыки":
        result_list = select_skills(data, impact)
    else:
        for item in data:
            if item[impact[0]] == impact[1]:
                result_list.append(item)
    return result_list


def select_skills(data, impact):
    impact_skills = impact[1].split(", ")
    impact_skills = list(impact_skills)
    out = []
    for item in data:
        count = []
        count_add(count, impact_skills, item)
        if len(count) == len(impact_skills):
            out.append(item)
    return out


def table_filler(data, pretty_table):
    for n, layer in enumerate(data):
        layer = RightRow(layer)
        for key, val in layer.items():
            if len(val) > 100:
                layer[key] = val[:100] + "..."
            else:
                layer[key] = val
        pretty_table.add_row([n + 1,
                              layer["Название"],
                              layer["Описание"],
                              layer["Навыки"],
                              layer["Опыт работы"],
                              layer["Премиум-вакансия"],
                              layer["Компания"],
                              layer["Оклад"],
                              layer["Название региона"],
                              layer["Дата публикации вакансии"]])


def sort_check(check_text):
    if check_text == "Нет":
        return False, None
    elif check_text == "Да":
        return True, None
    return None, "Порядок сортировки задан некорректно"


def count_add(count, impact_skills, item):
    for impact_skill in impact_skills:
        skills = item["Навыки"].split("\n")
        for skill in skills:
            if skill == impact_skill:
                count.append(skill)


def data_recone(file, header):
    vacancy_data = filter(lambda item: len(item) == len(header) and "" not in item, file)
    # vacancy_data = (map(clean_string, item) for item in vacancy_data)
    vacancy_data = (dict(zip(header, map(string_to_FormatStr, item))) for item in vacancy_data)
    return vacancy_data


def clean_from_tags(text):
    sample = re.compile('<.*?>')
    text = re.sub(sample, '', text)
    new_text = text.split("\n")
    return new_text


def Key_skills_to_FormatStr(new_text):
    # Этот блок необходим только для Навыков, но для удобства сюда подаются все строки
    text = [" ".join(value.strip().split()) for value in new_text]
    new_text = "\n".join(text)
    return new_text


def CSV_File_Start(CSV_name, filt_parametre, SortParametre, sort_reserved,rows_parametre, col_parametre): #CSV_File_Start
    if filt_parametre != "":
        impact, answer = parametre_check(filt_parametre)
    else:
        impact = None
        answer = None
    if answer:
        print(answer)
        return

    if sort_reserved == "":
        sort_reserved = False
        answer = None
    else:
        sort_reserved, answer = sort_check(sort_reserved)
    if answer:
        print(answer)
        return

    if SortParametre == "":
        SortParametre = None
        answer = None
    else:
        SortParametre, answer = SortParametre_check(SortParametre)
    if answer:
        print(answer)
        return

    if len(rows_parametre) != 0:
        range_of_rows = [(int(n) - 1) for n in rows_parametre]
    else:
        range_of_rows = [None]

    if len(col_parametre) != 0:
        names_of_columns = col_parametre.split(", ")
    else:
        names_of_columns = None

    with open(CSV_name, "r", encoding="utf-8-sig") as f:
        if os.stat(f.name).st_size != 0:

            f = csv.reader(f, delimiter=",")
            # !!!!!!!!!!!!!!!!!!!!!!!!!
            header = list(map(string_to_FormatStr, next(f)))
            # !!!!!!!!!!!!!!!!!!!!!!!!
            data = list(data_recone(f, header))

            if len(data) != 0:
                table_print(data, range_of_rows, names_of_columns, impact, SortParametre, sort_reserved)
            else:
                return print('Нет данных')
        else: return print('Пустой файл')

layer_of_names = ["№", "Название",
                  "Описание", "Навыки",
                  "Опыт работы", "Премиум-вакансия",
                  "Компания", "Оклад",
                  "Название региона",
                  "Дата публикации вакансии"]

dictionary_translator = {"description": "Описание",
               "UZS": "Узбекский сум",
               "between1And3": "От 1 года до 3 лет",
               "GEL": "Грузинский лари",
               "key_skills": "Навыки",
               "experience_id": "Опыт работы",
               "EUR": "Евро",
               "premium": "Премиум-вакансия",
               "UAH": "Гривны",
               "salary_from": "Нижняя граница вилки оклада",
               "RUR": "Рубли",
                         "salary_gross": "Оклад указан до вычета налогов",
                         "KGS": "Киргизский сом",
                         "area_name": "Название региона",
                         "published_at": "Дата публикации вакансии",
                         "BYR": "Белорусские рубли",
                         "name": "Название",
                         "True": "Да",
                         "KZT": "Тенге",
                         "TRUE": "Да",
                         "False": "Нет",
                         "salary_to": "Верхняя граница вилки оклада",
                         "FALSE": "Нет",
                         "USD": "Доллары",
                         "noExperience": "Нет опыта",
                         "UZS": "Узбекский сум",
                         "employer_name": "Компания",
                         "between3And6": "От 3 до 6 лет",
                         "salary_currency": "Идентификатор валюты оклада",
                         "moreThan6": "Более 6 лет",
                         "AZN": "Манаты",
                         "salary": "Оклад"}

currency_to_rub = {"Тенге": 0.13,
                   "Гривны": 1.64,
                   "Белорусские рубли": 23.91,
                   "Манаты": 35.68,
                   "Доллары": 60.66,
                   "Рубли": 1,
                   "Грузинский лари": 21.74,
                   "Евро": 59.90,
                   "Киргизский сом": 0.76,
                   "Узбекский сум": 0.0055}

sign_of_exp = {"Более 6 лет": 3,
                     "От 3 до 6 лет": 2 ,
                     "От 1 года до 3 лет": 1,
                     "Нет опыта": 0}


CSV_File_Start(input("Введите название файла:"),
               input("Введите параметр фильтрации:"),
               input("Введите параметр сортировки:"),
               input("Обратный порядок сортировки (Да / Нет):"),
               input("Введите диапазон вывода:").split(),
               input("Введите требуемые столбцы:"))




"""
vacancies.csv  
Опыт работы: От 3 до 6 лет  
Оклад  
Нет  
10 20  
Название, Навыки, Опыт работы, Оклад

vacancies.csv

Оклад
Да
"""