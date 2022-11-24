def Declention_Names(x):  # определяем склонение (год/года/лет)
    if (x == 1 or x % 10 == 1) and x % 100 // 10 != 1:
        return f'{x} год'
    if (x > 1 and x < 5) or (x > 20 and str(x % 10) in '234' and x % 100 // 10 != 1):
        return f'{x} года'
    else:
        return f'{x} лет'

def Declention_money(x):  # определяем склонение (рубль/рублей/рубля)
    if (x == 1 or x % 10 == 1) and x % 100 // 10 != 1:
        return f'{x} рубль'
    if (x > 1 and x < 5) or (x > 20 and str(x % 10) in '234' and x % 100 // 10 != 1):
        return f'{x} рубля'
    else:
        return f'{x} рублей'

VacancyN = input('Введите название вакансии: ')
while VacancyN == '':
    VacancyN = input('Данные некорректны, повторите ввод\nВведите название вакансии: ')

VacancyOp = input('Введите описание вакансии: ')
while VacancyOp == '':
    VacancyOp = input('Данные некорректны, повторите ввод\nВведите описание вакансии: ')

AgeOfExp = input('Введите требуемый опыт работы (лет): ')
while not(AgeOfExp.isdigit()):
    AgeOfExp = (input('Данные некорректны, повторите ввод\nВведите требуемый опыт работы (лет): '))

ZpFrom = input('Введите нижнюю границу оклада вакансии: ')
while not(ZpFrom.isdigit()):
    ZpFrom = (input('Данные некорректны, повторите ввод\nВведите нижнюю границу оклада вакансии: '))

ZpTo = input('Введите верхнюю границу оклада вакансии: ')
while not(ZpTo.isdigit()):
    ZpTo = (input('Данные некорректны, повторите ввод\nВведите верхнюю границу оклада вакансии: '))

Timetable = input('Есть ли свободный график (да / нет): ')
while Timetable != 'да' and Timetable != 'нет': Timetable = (
    input('Данные некорректны, повторите ввод\nЕсть ли свободный график (да / нет): '))

VacancyPr = input('Является ли данная вакансия премиум-вакансией (да / нет): ')
while VacancyPr != 'да' and VacancyPr != 'нет': VacancyPr = (
    input('Данные некорректны, повторите ввод\nЯвляется ли данная вакансия премиум-вакансией (да / нет): '))

Mid_ZP = (int(ZpTo) + int(ZpFrom)) / 2

print(VacancyN)
print('Описание: ' + VacancyOp)
print('Требуемый опыт работы: ' + Declention_Names(int(AgeOfExp)))
print('Средний оклад: ' + Declention_money(int(Mid_ZP)))
print('Свободный график: ' + Timetable)
print('Премиум-вакансия: ' + VacancyPr)










