import json
from abc import ABC, abstractmethod

from settings import LIST_WITH_JSON_PATH


class AbstractClassAPI(ABC):

    __url: str

    @abstractmethod
    def get_vacancies(self, parameters: dict) -> list:
        pass

    @abstractmethod
    def format_data(self, data: list) -> list:
        pass


class AbstractClassFileManager(ABC):

    path_to_main_file: str
    list_paths: list = LIST_WITH_JSON_PATH

    @abstractmethod
    def save_data(self) -> None:
        pass

    @staticmethod
    def get_data_vacancy() -> list:
        """ Метод для получения данных из кэш файлов json """

        res = []

        for path in LIST_WITH_JSON_PATH:
            with open(path, 'r', encoding='utf-8') as file:
                try:
                    res.extend(json.load(file))
                except json.decoder.JSONDecodeError:
                    print(f'Вероятно 1 из платформ не отработала корректно(json файл пуст {path})')
                    pass

        return res

    def clear_data(self) -> None:
        open(self.path_to_main_file, 'w').close()


class AbstractClassMenu(ABC):

    @abstractmethod
    def show_menu(self):
        pass
