import csv

from models.absclasses import AbstractClassFileManager
from settings import path_to_all_vacancy_csv


class CsvSaver(AbstractClassFileManager):
    """ Класс для работы с csv """

    path_to_main_file: str = path_to_all_vacancy_csv

    def save_data(self) -> None:
        """ Метод для сохранения данных в основной csv файл из кэшей если юзеру они понадобились """
        list_vacancy = self.get_data_vacancy()

        with open(self.path_to_main_file, 'w', encoding='utf-8', newline='') as file:
            file = csv.writer(file, delimiter='\t')
            file.writerow(['name', 'url', 'salary', 'experience', 'requirements', 'city'])
            file.writerows([[vacancy['name'],
                             vacancy['url'],
                             vacancy['salary'],
                             vacancy['experience'],
                             vacancy['requirements'],
                             vacancy['city']]
                            for vacancy in list_vacancy])
