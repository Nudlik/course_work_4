from models.headhunter import HeadHunterAPI
from models.superjob import SuperJobAPI
from models.vacancy import Vacancy
from models.jsonsaver import JsonSaver


def main():
    user_find_text = input('Введите слово для поиска по которому будем искать вакансии: ').lower().strip()
    count_pages = int(input('Введите количество страниц для парсинга(на 1ой странице будет 10 вакансий): ').strip())
    list_platforms = [HeadHunterAPI, SuperJobAPI]
    for platform in list_platforms:
        platform = platform(user_find_text)
        platform.save_data(count_pages)


if __name__ == '__main__':
    main()
