import requests

from models.absclasses import AbstractClassAPI


class HeadHunterAPI(AbstractClassAPI):
    """ Класс для работы с API hh.ru для поиска вакансий """

    url: str = r'https://api.hh.ru/vacancies/'
    USD_RATE: float = 60  # возможно надо дергать с другой апишки, это курс USD если что

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
                'text': find_text,
                'per_page': 10,
                'page': page
            }
            response = requests.get(self.url, params=query_parameters)
            res.extend(response.json()['items'])

        return res

    def get_vacancies_by_salary(self, find_text: str, pages: int = 1, salary: int = 0) -> list:
        res = []
        for page in range(pages):
            query_parameters = {
                'text': find_text,
                'per_page': 10,
                'page': page,
                'only_with_salary': True,
                'salary': salary
            }
            response = requests.get(self.url, params=query_parameters)
            res.extend(response.json()['items'])

        return res
