from models.headhunter import HeadHunterAPI
from models.superjob import SuperJobAPI
from models.vacancy import Vacancy
from models.jsonsaver import JsonSaver


def main():
    json_saver = JsonSaver()
    user_find_text = input('Введите слово для поиска по которому будем искать вакансии: ').lower().strip()
    count_pages = int(input('Введите количество страниц для парсинга(на 1ой странице будет 10 вакансий): ').strip())

    list_platforms = [HeadHunterAPI, SuperJobAPI]

    for platform in list_platforms:
        platform = platform()
        data = platform.get_vacancies(user_find_text, count_pages)
        json_saver.rotate(platform, data)


if __name__ == '__main__':
    main()
