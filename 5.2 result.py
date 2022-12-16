import re
import prettytable
from prettytable import PrettyTable
import csv
import os

toRubCurrency = {"Манаты": 35.68,
                 "Белорусские рубли": 23.91,
                 "Евро": 59.90,
                 "Грузинский лари": 21.74,
                 "Киргизский сом": 0.76,
                 "Тенге": 0.13,
                 "Рубли": 1,
                 "Гривны": 1.64,
                 "Доллары": 60.66,
                 "Узбекский сум": 0.0055, }
layer_of_names = ["№", "Название",
                  "Описание", "Навыки",
                  "Опыт работы", "Премиум-вакансия",
                  "Компания", "Оклад",
                  "Название региона",
                  "Дата публикации вакансии"]
sign_of_exp = {"Более 6 лет": 3,
               "От 3 до 6 лет": 2,
               "От 1 года до 3 лет": 1,
               "Нет опыта": 0}


class DataSet:
    def __init__(self, f_Name):
        self.dictionary_translator = {"noExperience": "Нет опыта",
                                      "between1And3": "От 1 года до 3 лет",
                                      "between3And6": "От 3 до 6 лет",
                                      "moreThan6": "Более 6 лет",
                                      "AZN": "Манаты",
                                      "BYR": "Белорусские рубли",
                                      "EUR": "Евро",
                                      "GEL": "Грузинский лари",
                                      "KGS": "Киргизский сом",
                                      "KZT": "Тенге",
                                      "RUR": "Рубли",
                                      "UAH": "Гривны",
                                      "USD": "Доллары",
                                      "UZS": "Узбекский сум",
                                      "True": "Да",
                                      "False": "Нет",
                                      "FALSE": "Нет",
                                      "TRUE": "Да"}
        self.file_name = f_Name
        header, data = self.CSV_File_Start(f_Name)
        vacancies = self.CSV_filtData(header, data)
        vac_items = []
        for vacancy in vacancies:
            vac_items.append(Vacancy(vacancy))
        self.vacancies_objects = vac_items

    def CSV_File_Start(self, CSV_name):

        with open(CSV_name, "r", encoding="utf-8-sig") as f:
            if os.stat(f.name).st_size == 0:
                print('Пустой файл')
                exit()
            if os.stat(f.name).st_size <= 138:
                print('Нет данных')
                exit()
            f = csv.reader(f, delimiter=",")
            # !!!!!!!!!!!!!!!!!!!!!!!!!
            header = list(map(self.string_to_FormatStr, next(f)))
            # !!!!!!!!!!!!!!!!!!!!!!!!
            data = list(self.data_recone(f, header))
        return header, data

    def string_to_FormatStr(self, text):
        new_text = self.clean_from_tags(text)
        # Этот блок нужен для всех пунктов

        new_text = self.Key_skills_to_FormatStr(new_text)
        # А этот для навыков

        if new_text in self.dictionary_translator:
            out = self.dictionary_translator[new_text]
        else:
            out = new_text
        return out

    def clean_from_tags(self, text):
        sample = re.compile('<.*?>')
        text = re.sub(sample, '', text)
        new_text = text.split("\n")
        return new_text

    def Key_skills_to_FormatStr(self, new_text):
        # Этот блок необходим только для Навыков, но для удобства сюда подаются все строки
        skills = [" ".join(value.strip().split()) for value in new_text]
        new_text = "\n".join(skills)
        return new_text

    def data_recone(self, name, header):
        vacancy_data = filter(lambda item: len(item) == len(header) and "" not in item, name)
        # vacancy_data = (map(clean_string, item) for item in vacancy_data)
        vacancy_data = (list(map(self.string_to_FormatStr, item)) for item in vacancy_data)
        return vacancy_data

    def CSV_filtData(self, header, all_vacancies):
        list_of_vacancies = []
        for item in all_vacancies:
            new_vacancy = {}
            for num in range(len(header)):
                new_vacancy[header[num]] = self.string_to_FormatStr(item[num])
            list_of_vacancies.append(new_vacancy)
        return list_of_vacancies


class Vacancy:
    def __init__(self, vacancy_item):
        self.description = vacancy_item["description"]
        self.name = vacancy_item["name"]

        self.employer_name = vacancy_item["employer_name"]
        self.premium = vacancy_item["premium"]
        self.key_skills = vacancy_item["key_skills"]
        self.area_name = vacancy_item["area_name"]
        self.published_at = vacancy_item["published_at"]
        self.experience_id = vacancy_item["experience_id"]
        self.salary = Salary(
            vacancy_item["salary_from"], vacancy_item["salary_to"], vacancy_item["salary_gross"],
            vacancy_item["salary_currency"])
        self.employer_name = vacancy_item["employer_name"]

        self.experience_id = vacancy_item["experience_id"]

    def eng_names(self):  # Это менять порядком можно get_copy
        return Vacancy({"description": self.description, "salary_from": self.salary.salary_bottom,
                        "employer_name": self.employer_name, "area_name": self.area_name,

                        "name": self.name, "experience_id": self.experience_id,

                        "key_skills": self.key_skills, "premium": self.premium, "salary_to": self.salary.salary_upper,
                        "published_at": self.published_at, "salary_currency": self.salary.CurrencyOfSalary,
                        "salary_gross": self.salary.GrossOfSalary})

    def rus_names(self):  # Это менять порядком нельзя get_variables
        return {"Название": self.name, "Описание": self.description, "Навыки": self.key_skills,
                "Опыт работы": self.experience_id, "Премиум-вакансия": self.premium,
                "Компания": self.employer_name, "Оклад": self.salary,
                "Название региона": self.area_name, "Дата публикации вакансии": self.published_at}


class Salary:
    def get_salary_rub(self):
        s_from = float(self.salary_bottom)
        s_to = float(self.salary_upper)
        course_valute = toRubCurrency[self.CurrencyOfSalary]
        rubs = (int(s_from) + int(s_to)) / 2 * course_valute
        return rubs

    def __init__(self, bottom_sal, upper_sal, sal_gross, sal_currency):
        self.salary_bottom = bottom_sal
        self.salary_upper = upper_sal
        self.GrossOfSalary = sal_gross
        self.CurrencyOfSalary = sal_currency


class InputCorrect:
    def __init__(self, parametre_filtration, parametre_sorting, backwords, from_to, col_names):

        self.needed_columns = col_names
        self.diapason = from_to
        self.sort_attribute = parametre_sorting
        # self.filter_attribute = parametre_filtration.split(": ")
        self.filter_attribute = parametre_filtration
        self.backread = backwords

    def parametre_check(self):
        answer = None

        if self.filter_attribute != "":
            doublepoint_ind = self.filter_attribute.find(': ')

            if doublepoint_ind == (-1):
                answer = "Формат ввода некорректен"
            else:
                impact = (self.filter_attribute[:doublepoint_ind], self.filter_attribute[doublepoint_ind + 2:])
                if impact[0] not in ["Идентификатор валюты оклада"] + layer_of_names + [""]:
                    answer = "Параметр поиска некорректен"
        else:
            answer = None
        if answer:
            print(answer)
            exit()
        return

    def sort_check(self):
        if self.backread != "Да" and self.backread != "Нет" and self.backread != "":
            answer = "Порядок сортировки задан некорректно"
            print(answer)
            exit()

        if self.backread == "Да":
            self.backread = True
        else: self.backread = False
        return

    def SortParametre_check(self):
        answer = "Параметр сортировки некорректен" if self.sort_attribute not in layer_of_names + [""] else None
        if answer:
            print(answer)
            exit()
        return

    def sort_vacancies(self, data):
        if self.sort_attribute == "":
            return data
        elif self.sort_attribute == "Оклад":
            parametre = lambda vac: vac.salary.get_salary_rub()
        elif self.sort_attribute == "Опыт работы":
            parametre = lambda vac: sign_of_exp[vac.experience_id]
        elif self.sort_attribute == "Навыки":
            parametre = lambda vac: len(vac.key_skills.split("\n"))
        else:
            parametre = lambda vacancy: vacancy.rus_names()[self.sort_attribute]

        out = sorted(data, key=parametre, reverse=self.backread)
        return out

    def skip_vac(self, vacancy):
        doublepoint_ind = self.filter_attribute.find(': ')
        impact = (self.filter_attribute[:doublepoint_ind], self.filter_attribute[doublepoint_ind + 2:])
        is_to_pass = True

        if impact[0] == "Навыки":

            for e in impact[1].split(", "):
                if e not in vacancy.key_skills.split("\n"):
                    is_to_pass = False

        elif impact[0] == "Идентификатор валюты оклада":
            if impact[1] != vacancy.salary.CurrencyOfSalary:
                is_to_pass = False

        elif impact[0] == "Дата публикации вакансии":
            if impact[1] != self.time_to_format(vacancy.published_at):
                is_to_pass = False

        elif impact[0] == "Оклад":
            sal_range = [int(float(vacancy.salary.salary_bottom)), int(float(vacancy.salary.salary_upper))]

            if int(float(impact[1])) > sal_range[1] or int(float(impact[1])) < sal_range[0]:
                is_to_pass = False

        elif impact[0] in vacancy.rus_names():
            if impact[1] != vacancy.rus_names()[impact[0]]:
                is_to_pass = False
        return is_to_pass


    def printVacs(self, vacs):
        table = PrettyTable()
        table.hrules = prettytable.ALL
        table.align = 'l'
        table.field_names = layer_of_names
        table.max_width = 20
        num = 1

        sorted_vacs = self.sort_vacancies(vacs)

        for newVac in sorted_vacs:
            vacancy_formated = self.formatter(newVac)
            if not self.skip_vac(newVac):
                continue

            row = [value[:100] + "..." if len(value) > 100 else value
                   for value in vacancy_formated.rus_names().values()]

            row.insert(0, num)
            table.add_row(row)
            num += 1
        if num == 1:
            print("Ничего не найдено")
            exit()

        start, end = self.set_boundaries(num - 1)

        self.needed_columns = self.needed_columns.split(", ")
        if self.needed_columns[0] == "":
            table = table.get_string(start=start, end=end)
        else:
            self.needed_columns.insert(0, "№")
            table = table.get_string(start=start, end=end, ﬁelds=self.needed_columns)
        print(table)

    def formatter(self, vac):
        newVac = vac.eng_names()
        newVac.salary = self.sal_to_format(vac)
        newVac.published_at = self.time_to_format(vac.published_at)
        return newVac

    def sal_to_format(self, vac):
        bottom = self.money_to_format(vac.salary.salary_bottom)
        upper = self.money_to_format(vac.salary.salary_upper)
        is_tax_free = "Без вычета налогов" if vac.salary.GrossOfSalary == "Да" else "С вычетом налогов"

        return f"{bottom} - {upper} ({vac.salary.CurrencyOfSalary}) ({is_tax_free})"

    def set_boundaries(self, count):
        self.diapason = self.diapason.split(" ")
        start = 0
        end = count

        if self.diapason[0] == "":
            pass
        elif len(self.diapason) > 0:
            start = int(self.diapason[0]) - 1
            if len(self.diapason) == 2:
                end = int(self.diapason[1]) - 1

        return start, end

    def money_to_format(self, salar):
        salar = str(int(float(salar)))

        deleted_point = salar[:salar.find('.')] if '.' in salar else salar

        first_space = deleted_point[:len(deleted_point) - 3] if len(deleted_point) > 3 else ''
        second_spase = first_space[:len(first_space) - 3] if len(first_space) > 3 else ''

        units = deleted_point[len(first_space):]
        thousands = first_space[len(second_spase):]
        millions = second_spase

        if millions:
            return f"{millions} {thousands} {units}"
        elif thousands:
            return f"{thousands} {units}"
        else:
            return units

    def time_to_format(self, date):
        return f"{date[8:10]}.{date[5:7]}.{date[:4]}"


file = input("Введите название файла: ")
parametre_filtration = input("Введите параметр фильтрации: ")
parametre_sorting = input("Введите параметр сортировки: ")
backwords = input("Обратный порядок сортировки (Да / Нет): ")
from_to = input("Введите диапазон вывода: ")
col_names = input("Введите требуемые столбцы: ")

correctInput = InputCorrect(parametre_filtration, parametre_sorting, backwords, from_to, col_names)
correctInput.parametre_check()
correctInput.sort_check()
correctInput.SortParametre_check()
dataset = DataSet(file)
correctInput.printVacs(dataset.vacancies_objects)

"""
vacancies.csv
Опыт работы: От 3 до 6 лет
Оклад
Нет
10 20
Название, Описание, Навыки, Опыт работы, Оклад
"""
"""
vacancies.csv

Компания



"""