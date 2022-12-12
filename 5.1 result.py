import csv
from var_dump import var_dump
import csv
import re
import os


def string_to_FormatStr(text):
    new_text = clean_from_tags(text)
    # Этот блок нужен для всех пунктов

    new_text = Key_skills_to_FormatStr(new_text)
    # А этот для навыков

    return new_text

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


def CSV_File_Start(CSV_name): #CSV_File_Start

    with open(CSV_name, "r", encoding="utf-8-sig") as f:
        if os.stat(f.name).st_size == 0:
            print('Пустой файл')
            exit()
        f = csv.reader(f, delimiter=",")
            # !!!!!!!!!!!!!!!!!!!!!!!!!
        header = list(map(string_to_FormatStr, next(f)))
            # !!!!!!!!!!!!!!!!!!!!!!!!
        data = list(data_recone(f, header))
    return header, data


def CSV_filtData(header, all_vacancies):
    list_of_vacancies = []
    for item in all_vacancies:
        new_vacancy = {}
        for num in range(len(header)):
            new_vacancy[header[num]] = string_to_FormatStr(item[num])
        list_of_vacancies.append(new_vacancy)
    return list_of_vacancies


def data_recone(file, header):
    vacancy_data = filter(lambda item: len(item) == len(header) and "" not in item, file)
    # vacancy_data = (map(clean_string, item) for item in vacancy_data)
    vacancy_data = (list(map(string_to_FormatStr, item)) for item in vacancy_data)
    return vacancy_data

class Salary:
    def __init__(self, currency, gross, To, From):
        self.salary_from = From
        self.salary_to = To
        self.salary_gross = gross
        self.salary_currency = currency


class DataSet:
    def __init__(self, file):
        vac_items = []
        header, data = CSV_File_Start(file)
        vacancies = CSV_filtData(header, data)
        for vacancy in vacancies:
            vac_items.append(Vacancy(vacancy))
        # сперва название файла
        self.file_name = file
        # потом записать данные
        self.vacancies_objects = vac_items



class Vacancy:
    def __init__(self, vacancy):
        self.name = vacancy["name"]
        self.description = vacancy["description"]
        key_skills = vacancy["key_skills"].split('\n')
        self.key_skills = key_skills
        self.experience_id = vacancy["experience_id"]
        self.premium = vacancy["premium"]
        self.employer_name = vacancy["employer_name"]
        self.salary = Salary(
            vacancy["salary_currency"], vacancy["salary_gross"], vacancy["salary_to"], vacancy["salary_from"])
        self.area_name = vacancy["area_name"]
        self.published_at = vacancy["published_at"]
        self.employer_name = vacancy["employer_name"]
        self.published_at = vacancy["published_at"]


def Begin_program():
    name = input("Введите название файла: ")
    filterParam = input("Введите параметр фильтрации: ")
    sortParam = input("Введите параметр сортировки: ")
    isReverse = input("Обратный порядок сортировки (Да / Нет): ")
    diap = input("Введите диапазон вывода: ")
    columns = input("Введите требуемые столбцы: ")
    var_dump(DataSet(name))



Begin_program()