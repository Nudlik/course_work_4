import requests

from models.absclasses import AbstractClassAPI


class HeadHunterAPI(AbstractClassAPI):
    """ Класс для работы с API hh.ru для поиска вакансий """

    __url: str = r'https://api.hh.ru/vacancies/'
    USD_RATE: float = 60  # возможно надо дергать с другой апишки, это курс USD если что

    def get_vacancies(self, find_text: str, pages: int = 1) -> list:
        """
        Метод для получения списка вакансий
        :param find_text: искомое слово
        :param pages: количество страниц которые нужно получить
        :return: список вакансий
        """
        query_parameters = {
            'text': find_text,
            'per_page': 10,
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
            'text': find_text,
            'per_page': 10,
            'only_with_salary': True,
            'salary': salary
        }
        return self.__get_vacancies_universl(pages, query_parameters)

    def __get_vacancies_universl(self, pages: int = 1, params: dict = None) -> list:
        """ Вспомогательный метод для получения списка вакансий """

        res = []
        for page in range(pages):
            query_parameters = params
            query_parameters['page'] = page
            response = requests.get(self.__url, params=query_parameters)
            res.extend(response.json()['items'])

        return res
