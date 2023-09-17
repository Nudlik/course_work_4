import requests

from models.absclasses import AbstractClassAPI
from models.optiondictparams import OptionDictParams
from settings import API_KEY_SUPERJOB


class SuperJobAPI(AbstractClassAPI):
    """ Класс для работы с API superjob.ru для поиска вакансий """

    __url: str = 'https://api.superjob.ru/2.0/vacancies/'
    __headers: dict = {'X-Api-App-Id': API_KEY_SUPERJOB}

    def get_vacancies(self, option_params: OptionDictParams) -> list:
        """
        Метод для получения списка вакансий
        :param option_params: класс OptionDictParams для хранения параметров
        :param parameters: словарик с параметрами поиска
        :return: список вакансий
        """

        keyword = option_params.text
        salary = option_params.salary
        city = option_params.city
        experience = option_params.experience
        pages = option_params.pages
        per_page = 10

        query_parameters = {
            'keyword': keyword,
            'count': per_page,
        }

        if salary:
            query_parameters['no_agreement'] = 1
            query_parameters['payment_from'] = salary

        if city:
            correct_city = self.check_city(city)
            if correct_city:
                query_parameters['t'] = [1, correct_city]
            else:
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
            response = requests.get(self.__url, params=query_parameters, headers=self.__headers)

            if response.status_code != 200:
                raise Exception('SuperJobAPI: Ошибка запроса вакансий, api не работает')

            response_json = response.json()
            response_list = response_json['objects']

            if not response_list:  # Сбрасываем фильтр по городам, я без понятия почему он не ищет по ид
                print('Фильтр городов не был применен к SuperJobAPI'); print('Не', end=' ')
                query_parameters['t'] = []
                query_parameters['town'] = ''
                response = self.__get_vacancies_universl(pages, query_parameters)
                res.extend(response)
            else:
                res.extend(response_list)

            if res:
                return res
            else:
                raise Exception('SuperJobAPI: Не найдено ни одной вакансии')

    def check_city(self, city_title: str) -> int | None:
        """ Метод для проверки введенного города """

        url = 'https://api.superjob.ru/2.0/towns/'
        response = requests.get(url, headers=self.__headers)

        if response.status_code != 200:
            raise Exception('SuperJobAPI: Ошибка запроса городов, api не работает')

        response_json = response.json()['objects']
        for city in response_json:
            if city['title'] == city_title:
                return city['id']
