import csv
import time

names = 0
min = 1
max = 2
currency = 3
space = 4
publicateTime = 5


moneyValue = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}


def csv_reader(fileName):
    global lenghtOfVacancies
    value = False
    with open(fileName, encoding='utf-8') as file:
        reader = csv.reader(file)
        for string in reader:
            if not value:
                value = True
                names = string.index("name")
                min = string.index("salary_from")
                max = string.index("salary_to")
                currency = string.index("salary_currency")
                space = string.index("area_name")
                publicateTime = string.index("published_at")
            else:
                row = string.copy()
                if all(row):
                    year = int(string[publicateTime].split("-")[0])
                    salaryCurrency = (int(float(string[max])) + int(float(string[min]))) * moneyValue[string[currency]] // 2
                    naming = string[names]
                    area = string[space]
                    sum[year] = sum.get(year, 0) + salaryCurrency
                    lenght[year] = lenght.get(year, 0) + 1
                    if name in naming:
                        quantity[year] = quantity.get(year, 0) + salaryCurrency
                        currencyLenght[year] = currencyLenght.get(year, 0) + 1
                    if area not in cities:
                        cities.append(area)
                    amountOfCities[area] = amountOfCities.get(area, 0) + salaryCurrency
                    lenghtOfCities[area] = lenghtOfCities.get(area, 0) + 1
                    lenghtOfVacancies += 1


pubTime = time.time()
nameOfFile = input("Введите название файла: ")
name = input("Введите название профессии: ")
year = [i for i in range(2007, 2023)]
sum = {}
lenght = {}
quantity = {}
currencyLenght = {}
cities = []
amountOfCities = {}
lenghtOfCities = {}
lenghtOfVacancies = 0
csv_reader(nameOfFile)


for i in year:
    if sum.get(i, None):
        sum[i] = int(sum[i] // lenght[i])
    if quantity.get(i, None):
        quantity[i] = int(quantity[i] // currencyLenght[i])


for j in cities:
    amountOfCities[j] = int(amountOfCities[j] // lenghtOfCities[j])


citiesOfInterest = [city for city in cities if lenghtOfCities[city] >= lenghtOfVacancies // 100]
amountOfCity = {key: amountOfCities[key] for key in sorted(citiesOfInterest, key=lambda x: amountOfCities[x], reverse=True)[:10]}
section = {key: float("{:.4f}".format(lenghtOfCities[key] / lenghtOfVacancies)) for key in sorted(citiesOfInterest, key=lambda x: lenghtOfCities[x] / lenghtOfVacancies, reverse=True)[:10]}


print("Динамика уровня зарплат по годам:", sum)

print("Динамика количества вакансий по годам:", lenght)

if not len(quantity):
    quantity[2022] = 0

print("Динамика уровня зарплат по годам для выбранной профессии:", quantity)

if not len(currencyLenght):
    currencyLenght[2022] = 0

print("Динамика количества вакансий по годам для выбранной профессии:", currencyLenght)

print("Уровень зарплат по городам (в порядке убывания):", amountOfCity)

print("Доля вакансий по городам (в порядке убывания):", section)

result = time.time()