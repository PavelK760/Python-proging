import csv
import re

def сsv_reader(file_name):
    with open(file_name, encoding='UTF-8-sig') as csvfile:
        file = csv.reader(csvfile)
        header = next(file)
        list = []
        for item in file:
            if '' not in item and len(item) == len(header):
                list.append(item)
        return header, list

def elements_replacer(word):
    for j in range(len(word)):
        word[j] = re.sub(r'<[^>]*>', '', word[j])
        if '\n' in word[j]: word[j] = word[j].replace('\n', ', ')
        word[j] = ' '.join(word[j].split())
        if word[j] == 'True':
            word[j] = "Да"
        elif word[j] == 'False':
            word[j] = "Нет"

def dic_filler(NewText, dict_vacansies, list_naming, word):
    for key, Val in zip(list_naming, word):
        dict_vacansies[key] = Val
    NewText.append(dict_vacansies)

def csv_filer(reader, list_naming):
    NewText = []
    for word in reader:
        dict_vacansies = {}
        elements_replacer(word)
        dic_filler(NewText, dict_vacansies, list_naming, word)
    return NewText



def print_vacancies(data_vacancies, dic_naming):
    for value in data_vacancies:
        for j in dic_naming:
            print(f'{dic_naming[j]}: {value[j]}')
        print()


#Прописать все значения, которые придётся заменить, проще в словари, так что так и поступим
dic_keys_translations = {'name' : "Название", 'description' : "Описание", 'key_skills' : "Навыки",
              'experience_id' : "Опыт работы", 'premium' : "Премиум-вакансия",
              'employer_name' : "Компания", 'salary_from' : "Нижняя граница вилки оклада",
              'salary_to': "Верхняя граница вилки оклада", 'salary_gross': "Оклад указан до вычета налогов",
              'salary_currency': "Идентификатор валюты оклада", 'area_name': "Название региона",
              'published_at': "Дата и время публикации вакансии"}
#чисто строчки с вызовами методов
header, vacancies_data = сsv_reader(input())
vacansies_main = csv_filer(vacancies_data, header)
print_vacancies(vacansies_main, dic_keys_translations)