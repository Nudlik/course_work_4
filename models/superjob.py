import requests

from models.absclasses import AbstractClassAPI
from settings import API_KEY_SUPERJOB


class SuperJobAPI(AbstractClassAPI):
    """ Класс для работы с API superjob.ru для поиска вакансий """

    __url: str = 'https://api.superjob.ru/2.0/vacancies/'
    headers: dict = {'X-Api-App-Id': API_KEY_SUPERJOB}

    def get_vacancies(self, find_text: str, pages: int = 1) -> list:
        """
        Метод для получения списка вакансий
        :param find_text: искомое слово
        :param pages: количество страниц которые нужно получить
        :return: список вакансий
        """
        query_parameters = {
            'keyword': find_text,
            'count': 10,
        }
        return self.__get_vacancies_universl(pages, query_parameters)

    def get_vacancies_by_salary(self, find_text: str, pages: int = 1, salary: int = 0) -> list:
        """
         Метод для получения списка вакансий по зарплате
        :param find_text: искомое слово
        :param pages: количество страниц которые нужно получить
        :param salary: ожидаемая зарплата
        :return: список вакансий
        """
        query_parameters = {
            'keyword': find_text,
            'count': 10,
            'no_agreement': 1,
            'payment_from': salary
        }
        return self.__get_vacancies_universl(pages, query_parameters)

    def __get_vacancies_universl(self, pages: int = 1, params: dict = None) -> list:
        """ Вспомогательный метод для получения списка вакансий """

        res = []
        for page in range(pages):
            query_parameters = params
            query_parameters['page'] = page
            response = requests.get(self.__url, params=query_parameters, headers=self.headers)
            res.extend(response.json()['objects'])

        return res
