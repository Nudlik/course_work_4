import json
import re
from functools import wraps

from models.absclasses import AbstractClassJsonSaver
from models.headhunter import HeadHunterAPI
from models.superjob import SuperJobAPI
from models.vacancy import Vacancy
from settings import path_to_hh_vacancy, path_to_sj_vacancy, path_to_all_vacancy, LIST_WITH_JSON_PATH


class JsonSaver(AbstractClassJsonSaver):
    """ Класс для работы с json """

    __path_to_main_json: str = path_to_all_vacancy
    __list_paths: list = LIST_WITH_JSON_PATH

    def rotate(self, platform: HeadHunterAPI | SuperJobAPI, data: list) -> None:
        """ Метод для выборки и сохранения json """

        if isinstance(platform, HeadHunterAPI):
            self.path_to_json = path_to_hh_vacancy
            self.clear_data(self.path_to_json)
            self.save_data_hh(data)
        elif isinstance(platform, SuperJobAPI):
            self.path_to_json = path_to_sj_vacancy
            self.clear_data(self.path_to_json)
            self.save_data_sj(data)

    def save_data_hh(self, data: list) -> None:
        """ Метод для сохранения в json данных с HeadHunter """

        with open(self.path_to_json, 'a', encoding='utf-8') as file:
            lst = []

            for page in range(len(data)):
                vacancy = data[page]

                salary = vacancy['salary']
                if isinstance(salary, dict):
                    currency = salary['currency']
                    from_ = salary['from']
                    if currency == 'USD':
                        salary = from_ * HeadHunterAPI.USD_RATE
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

            json.dump(lst, file, indent=4, ensure_ascii=False)

    def save_data_sj(self, data: list) -> None:
        """ Метод для сохранения в json данных с SuperJob """

        with open(self.path_to_json, 'a', encoding='utf-8') as file:
            lst = []
            for page in range(len(data)):
                vacancy = data[page]

                requirements = re.sub(r'[\n\t•]', '', vacancy['candidat'])[:170] + '...'

                lst.append({
                    'name': vacancy['profession'],
                    'url': vacancy['link'],
                    'salary': vacancy['payment_from'],
                    'experience': vacancy['experience']['title'],
                    'requirements': requirements,
                    'city': vacancy['town']['title']
                })

            json.dump(lst, file, indent=4, ensure_ascii=False)

    @staticmethod
    def decorate_json_except(func):
        """
        Декоратор для обработки исключений, возникающих при работе с JSON-файлами.
        :param func: Функция, которую нужно обернуть декоратором.
        :return: Результат выполнения функции `func`
        """

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except json.decoder.JSONDecodeError:
                print('Json файл пуст, выберите параметры для поиска и начните парсинг')
                return []
            except TypeError:
                print('Сначала спарсите а потом работайте с данными')
            except FileNotFoundError:
                print('Json файл не найден')
            except Exception as e:
                print(e)
            else:
                return res

        return inner

    @decorate_json_except
    def get_data_vacancy(self) -> list:
        """ Метод для получения данных из кэш файлов json """

        res = []
        for path in self.__list_paths:
            with open(path, 'r', encoding='utf-8') as file:
                try:
                    res.extend(json.load(file))
                except json.decoder.JSONDecodeError:
                    print(f'Вероятно 1 из платформ не отработала корректно(json файл пуст {path})')
                    pass

        return res

    @decorate_json_except
    def save_data_to_json(self) -> None:
        """ Метод для сохранения данных в основной json из кэшей если юзеру они понадобились """

        res = []
        for path in self.__list_paths:
            with open(path, 'r', encoding='utf-8') as file:
                try:
                    res.extend(json.load(file))
                except json.decoder.JSONDecodeError:
                    print(f'Вероятно 1 из платформ не отработала корректно(json файл пуст {path})')
                    pass

        if res:
            json.dump(res, open(self.__path_to_main_json, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

    def get_data_to_vacancy(self, data: list) -> list:
        """
        Метод для преобразования данных из json в объекты Vacancy
        :param data: список с вакансиями
        :return: список объектов list[Vacancy]
        """

        res = []
        data_vacancy = data
        for vacancy in data_vacancy:
            vacancy = Vacancy(name=vacancy['name'],
                              url=vacancy['url'],
                              salary=vacancy['salary'],
                              experience=vacancy['experience'],
                              requirements=vacancy['requirements'],
                              city=vacancy['city'])
            res.append(vacancy)

        return res

    def sorted_by_salary(self) -> list:
        """ Метод для сортировки вакансий по зарплате """

        return sorted(self.get_data_vacancy(), key=lambda x: x['salary'])

    @staticmethod
    def clear_cash() -> None:
        """ Метод для очистки кэша json """

        [open(path, 'w').close() for path in LIST_WITH_JSON_PATH]
