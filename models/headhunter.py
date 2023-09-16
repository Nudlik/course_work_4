import requests

from models.absclasses import AbstractClassAPI


class HeadHunterAPI(AbstractClassAPI):
    """ Класс для работы с API hh.ru для поиска вакансий """

    __url: str = r'https://api.hh.ru/vacancies/'
    USD_RATE: float = 60  # возможно надо дергать с другой апишки, это курс USD если что

    def get_vacancies(self, parameters: dict) -> list:
        """
        Метод для получения списка вакансий
        :param parameters: словарик с параметрами поиска
        :return: список вакансий
        """

        text = parameters.get('text')
        salary = parameters.get('salary')
        city = parameters.get('city')
        experience = parameters.get('expirience')
        pages = parameters.get('pages')
        per_page = 10

        query_parameters = {
            'text': text,
            'per_page': per_page,
        }

        if salary:
            query_parameters['only_with_salary'] = True
            query_parameters['salary'] = salary

        if city:
            city = self.check_city(city.capitalize())
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
            res.extend(response.json()['items'])

        return res

    def check_city(self, city):
        """ Метод для проверки введенного города """

        url = 'https://api.hh.ru/areas'

        response = requests.get(url)
        response_json = response.json()

        return self.find_city(city, response_json)

    def find_city(self, city_name: str, areas: dict) -> int | None:
        """
        Рекурсивный метод для поиска города по названию
        :param city_name: название города
        :param areas: словарик с городами и определенной структурой смотреть
        (https://github.com/hhru/api/blob/master/docs/areas.md#areas)
        :return: id города или None
        """

        for area in areas:
            if area['name'] == city_name:
                return area['id']
            elif area['areas']:
                result = self.find_city(city_name, area['areas'])
                if result:
                    return result
