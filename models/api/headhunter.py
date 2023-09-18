import re

import requests

from models.absclasses import AbstractClassAPI
from models.optiondictparams import OptionDictParams


class HeadHunterAPI(AbstractClassAPI):
    """ Класс для работы с API hh.ru для поиска вакансий """

    __url: str = r'https://api.hh.ru/vacancies/'
    __USD_RATE: float = 60  # возможно надо дергать с другой апишки, это курс USD если что

    def get_vacancies(self, option_params: OptionDictParams) -> list:
        """
        Метод для получения списка вакансий
        :param option_params: класс OptionDictParams для хранения параметров
        :return: список вакансий
        """

        text = option_params.text
        salary = option_params.salary
        city = option_params.city
        experience = option_params.experience
        pages = option_params.pages
        per_page = 10

        query_parameters = {
            'text': text,
            'per_page': per_page,
        }

        if salary:
            query_parameters['only_with_salary'] = True
            query_parameters['salary'] = salary

        if city:
            city = self.check_city(city)
            query_parameters['area'] = city

        if experience:
            query_parameters['experience'] = experience

        return self.__get_vacancies_universl(pages, query_parameters)

    def __get_vacancies_universl(self, pages: int = 1, params: dict = None) -> list:
        """ Вспомогательный метод для получения списка вакансий """

        res = []
        for page in range(pages):
            query_parameters = params
            query_parameters['page'] = page
            response = requests.get(self.__url, params=query_parameters)

            if response.status_code != 200:
                raise Exception('HeadHunterAPI: Ошибка запроса вакансий, api не работает')

            res.extend(response.json()['items'])

            if not res:
                raise Exception('HeadHunterAPI: Не найдено ни одной вакансии')

        return res

    def check_city(self, city):
        """ Метод для проверки введенного города """

        url = 'https://api.hh.ru/areas'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception('HeadHunterAPI: Ошибка запроса городов, api не работает')

        response_json = response.json()

        return self.find_city(city, response_json)

    def find_city(self, city_title: str, areas: dict) -> int | None:
        """
        Рекурсивный метод для поиска города по названию
        :param city_title: название города
        :param areas: словарик с городами и определенной структурой смотреть
        (https://github.com/hhru/api/blob/master/docs/areas.md#areas)
        :return: id города или None
        """

        for area in areas:
            if area['name'] == city_title:
                return area['id']
            elif area['areas']:
                result = self.find_city(city_title, area['areas'])
                if result:
                    return int(result)

    def format_data(self, data: list) -> list:
        """ Метод для форматирования данных в формате list[dict, ...] """

        lst = []

        for page in range(len(data)):
            vacancy = data[page]

            salary = vacancy['salary']
            if isinstance(salary, dict):
                currency = salary['currency']
                from_ = salary['from']
                if currency == 'USD':
                    salary = from_ * HeadHunterAPI.__USD_RATE
                elif from_ is None:
                    salary = 0
                else:
                    salary = from_
            else:
                salary = 0

            requirements = vacancy['snippet']['responsibility']
            requirements = re.sub(r'<.*?>', '', requirements) if requirements else 'Не указано'

            lst.append({
                'name': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary': salary,
                'experience': vacancy['experience']['name'],
                'requirements': requirements,
                'city': vacancy['area']['name']
            })

        return lst
