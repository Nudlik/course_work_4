import json

from models.absclasses import AbstractClassFileManager
from settings import path_to_all_vacancy_json


class JsonSaver(AbstractClassFileManager):
    """ Класс для работы с json """

    path_to_main_file: str = path_to_all_vacancy_json

    def save_data(self) -> None:
        """ Метод для сохранения данных в основной json из кэшей если юзеру они понадобились """

        with open(self.path_to_main_file, 'w', encoding='utf-8') as file:
            json.dump(self.get_data_vacancy(), file, indent=4, ensure_ascii=False)
