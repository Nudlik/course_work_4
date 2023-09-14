import requests

from models.absclasses import AbstractClassAPI


class HeadHunterAPI(AbstractClassAPI):

    url = r'https://api.hh.ru/vacancies/'
    USD_RATE = 60  # возможно надо дергать с другой апишки

    def get_vacancies(self, find_text, pages=1):
        res = []
        for page in range(pages):

            query_parameters = {
                'text': find_text,
                'per_page': 10,
                'page': page
            }

            response = requests.get(self.url, params=query_parameters)
            res.extend(response.json()['items'])

        return res
