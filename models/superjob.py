import requests

from models.absclasses import AbstractClassAPI
from settings import API_KEY_SUPERJOB


class SuperJobAPI(AbstractClassAPI):
    """ Класс для работы с API superjob.ru для поиска вакансий """

    url: str = 'https://api.superjob.ru/2.0/vacancies/'
    headers: dict = {'X-Api-App-Id': API_KEY_SUPERJOB}

    def get_vacancies(self, find_text: str, pages: int = 1) -> list:
        """
        Метод для получения списка вакансий
        :param find_text: искомое слово
        :param pages: количество страниц которые нужно получить
        :return: список вакансий
        """

        res = []
        for page in range(pages):
            query_parameters = {
                'keyword': find_text,
                'count': 10,
                'page': page
            }
            response = requests.get(self.url, params=query_parameters, headers=self.headers)
            res.extend(response.json()['objects'])

        return res

    def get_vacancies_by_salary(self, find_text: str, pages: int = 1, salary: int = 0) -> list:
        res = []
        for page in range(pages):
            query_parameters = {
                'keyword': find_text,
                'count': 10,
                'page': page,
                'no_agreement': 1,
                'payment_from': salary
            }
            response = requests.get(self.url, params=query_parameters, headers=self.headers)
            res.extend(response.json()['objects'])

        return res
