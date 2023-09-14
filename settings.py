import os


path_to_all_vacancy = os.path.join(os.path.dirname(__file__), 'data', 'all_vacancy.json')
path_to_hh_vacancy = os.path.join(os.path.dirname(__file__), 'data', 'hh_vacancy.json')
path_to_sj_vacancy = os.path.join(os.path.dirname(__file__), 'data', 'sj_vacancy.json')

API_KEY_SUPERJOB = os.getenv('SUPERJOB_API_KEY')
