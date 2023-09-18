from models.absclasses import AbstractClassFileManager
from models.vacancy import Vacancy
from settings import path_to_all_vacancy_txt


class TxtSaver(AbstractClassFileManager):
    """ Класс для работы с txt """

    path_to_main_file: str = path_to_all_vacancy_txt

    def save_data(self) -> None:
        """ Метод для сохранения данных в основной txt файл из кэшей если юзеру они понадобились """

        list_vacancy = self.get_data_vacancy()

        with open(self.path_to_main_file, 'w', encoding='utf-8') as file:
            [print(Vacancy(**vacancy), file=file, end='\n\n') for vacancy in list_vacancy]
