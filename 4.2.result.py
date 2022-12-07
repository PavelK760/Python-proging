import os
from prettytable import PrettyTable
import csv
import re


def time_to_format(time: str):
    return f"{time[8:10]}.{time[5:7]}.{time[:4]}"


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


def CSV_File_Start(CSV_name, filt_parametre, rows_parametre, col_parametre):
    if filt_parametre != "":
        impact, answer = parametre_check(filt_parametre)
    else:
        impact = None
        answer = None

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

            file = csv.reader(f, delimiter=",")
            # !!!!!!!!!!!!!!!!!!!!!!!!!
            header = list(map(string_to_FormatStr, next(file)))
            # !!!!!!!!!!!!!!!!!!!!!!!!
            data = list(data_recone(file, header))

            if len(data) != 0:
                table_print(data, range_of_rows, names_of_columns, impact)
            else:
                return print('Нет данных')

        else:
            return print('Пустой файл')


def money_to_format(salary: str):
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


def table_print(data, range_of_rows, names_of_columns, impact):
    pretty_table = PrettyTable()
    pretty_table.hrules = True
    pretty_table.align = 'l'
    pretty_table.field_names = row_titles
    pretty_table.max_width = 20

    if impact:
        data = select_by_parametre(data, impact)
        if len(data) != 0:
            table_filler(data, pretty_table)
        else:
            print("Ничего не найдено")
            return
    else:
        table_filler(data, pretty_table)

    t = pretty_table[slice(*(range_of_rows + [None]))]
    if names_of_columns:
        Fields = ["№"] + names_of_columns
    else:
        Fields = []
    print_table = t.get_string(fields=Fields)
    print(print_table)


def string_to_FormatStr(text):
    new_text = clean_from_tags(text)
    # Этот блок нужен для всех пунктов

    new_text = Key_skills_to_FormatStr(new_text)
    # А этот для навыков

    if new_text in transl_dict.keys():
        out = transl_dict[new_text]
    else:
        out = new_text
    return out


def clean_from_tags(text):
    sample = re.compile('<.*?>')
    text = re.sub(sample, '', text)
    new_text = text.split("\n")
    return new_text


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


def Key_skills_to_FormatStr(new_text):
    # Этот блок необходим только для Навыков, но для удобства сюда подаются все строки
    text = [" ".join(value.strip().split()) for value in new_text]
    new_text = "\n".join(text)
    return new_text


def count_add(count, impact_skills, item):
    for impact_skill in impact_skills:
        skills = item["Навыки"].split("\n")
        for skill in skills:
            if skill == impact_skill:
                count.append(skill)


def parametre_check(filt_parametre):
    doublepoint_ind = filt_parametre.find(': ')
    answer = None
    impact = None
    if doublepoint_ind == (-1):
        answer = "Формат ввода некорректен"
    else:
        impact = (filt_parametre[:doublepoint_ind], filt_parametre[doublepoint_ind + 2:])
        if impact[0] not in ["Идентификатор валюты оклада"] + row_titles:
            impact = None
            answer = "Параметр поиска некорректен"

    return impact, answer


def data_recone(file, header):
    vacancy_data = filter(lambda item: len(item) == len(header) and "" not in item, file)
    # vacancy_data = (map(clean_string, item) for item in vacancy_data)
    vacancy_data = (dict(zip(header, map(string_to_FormatStr, item))) for item in vacancy_data)
    return vacancy_data


row_titles = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания",
              "Оклад", "Название региона", "Дата публикации вакансии"]

transl_dict = {"description": "Описание",
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

CSV_File_Start(input(), input(), input().split(), input())

"""
vacancies.csv



"""