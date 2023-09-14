import json

from models.absclasses import AbstractClassJsonSaver
from models.headhunter import HeadHunterAPI
from models.superjob import SuperJobAPI
from settings import path_to_hh_vacancy, path_to_sj_vacancy


class JsonSaver(AbstractClassJsonSaver):

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
