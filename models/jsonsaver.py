import json

from models.absclasses import AbstractClassJsonSaver
from models.headhunter import HeadHunterAPI
from models.superjob import SuperJobAPI
from models.vacancy import Vacancy
from settings import path_to_hh_vacancy, path_to_sj_vacancy, path_to_all_vacancy, LIST_TO_JSON


class JsonSaver(AbstractClassJsonSaver):

    path_to_main_json = path_to_all_vacancy
    list_paths = LIST_TO_JSON

    def rotate(self, platform, data):
        if isinstance(platform, HeadHunterAPI):
            self.path_to_json = path_to_hh_vacancy
            self.clear_data(self.path_to_json)
            self.save_data_hh(data)
        elif isinstance(platform, SuperJobAPI):
            self.path_to_json = path_to_sj_vacancy
            self.clear_data(self.path_to_json)
            self.save_data_sj(data)

    def save_data_hh(self, data):
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
                requirements = requirements if requirements else 'Не указано'

                lst.append({
                    'name': vacancy['name'],
                    'url': vacancy['alternate_url'],
                    'salary': salary,
                    'experience': vacancy['experience']['name'],
                    'requirements': requirements,
                    'city': vacancy['area']['name']
                })

            json.dump(lst, file, indent=4, ensure_ascii=False)

    def save_data_sj(self, data):
        with open(self.path_to_json, 'a', encoding='utf-8') as file:
            lst = []
            for page in range(len(data)):
                vacancy = data[page]

                requirements = vacancy['candidat'][:100] + '...'

                lst.append({
                    'name': vacancy['profession'],
                    'url': vacancy['link'],
                    'salary': vacancy['payment_from'],
                    'experience': vacancy['experience']['title'],
                    'requirements': requirements,
                    'city': vacancy['town']['title']
                })

            json.dump(lst, file, indent=4, ensure_ascii=False)

    def get_data_vacancy(self):
        res = []
        for path in self.list_paths:
            with open(path, 'r', encoding='utf-8') as file:
                res.extend(json.load(file))
        return res

    def save_data_to_json(self):
        res = []
        for path in self.list_paths:
            with open(path, 'r', encoding='utf-8') as file:
                res.extend(json.load(file))

        json.dump(res, open(self.path_to_main_json, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

    def get_data_to_vacancy(self, data):
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

    def sorted_by_salary(self):
        return sorted(self.get_data_vacancy(), key=lambda x: x['salary'])
