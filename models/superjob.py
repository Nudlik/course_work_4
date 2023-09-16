import requests

from models.absclasses import AbstractClassAPI
from settings import API_KEY_SUPERJOB


class SuperJobAPI(AbstractClassAPI):
    """ Класс для работы с API superjob.ru для поиска вакансий """

    __url: str = 'https://api.superjob.ru/2.0/vacancies/'
    headers: dict = {'X-Api-App-Id': API_KEY_SUPERJOB}

    def get_vacancies(self, parameters: dict) -> list:
        """
        Метод для получения списка вакансий
        :param parameters: словарик с параметрами поиска
        :return: список вакансий
        """

        keyword = parameters.get('text')
        salary = parameters.get('salary')
        city = parameters.get('city')
        experience = parameters.get('expirience')
        pages = parameters.get('pages')
        per_page = 10

        query_parameters = {
            'keyword': keyword,
            'count': per_page,
        }

        if salary:
            query_parameters['no_agreement'] = 1
            query_parameters['payment_from'] = salary

        if city:
            query_parameters['town'] = city

        if experience:
            query_parameters['experience'] = experience

        return self.__get_vacancies_universl(pages, query_parameters)

    def __get_vacancies_universl(self, pages: int = 1, params: dict = None) -> list:
        """ Вспомогательный метод для получения списка вакансий """

        res = []
        for page in range(pages):
            query_parameters = params
            query_parameters['page'] = page
            response = requests.get(self.__url, params=query_parameters, headers=self.headers)
            res.extend(response.json()['objects'])
            if not res:
                raise Exception('SuperJobAPI: Не найдено ни одной вакансии')

        return res
