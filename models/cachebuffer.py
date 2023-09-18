import json
from functools import wraps

from models.absclasses import AbstractClassFileManager
from models.vacancy import Vacancy
from settings import path_to_all_vacancy_json, LIST_WITH_JSON_PATH


class CacheBuffer:
    """ Класс для работы с json """

    __path_to_main_file: str = path_to_all_vacancy_json
    __list_paths: list = LIST_WITH_JSON_PATH

    @staticmethod
    def save_cache(data: list, path: str) -> None:
        """ Метод для сохранения данных в кэш json """

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

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

        return AbstractClassFileManager.get_data_vacancy()

    @decorate_json_except
    def save_data(self) -> None:
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
            json.dump(res, open(self.__path_to_main_file, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

    @staticmethod
    def get_data_to_vacancy(data: list) -> list:
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
