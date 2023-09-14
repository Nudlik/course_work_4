from abc import ABC, abstractmethod


class AbstractClassAPI(ABC):

    url: str

    @abstractmethod
    def get_vacancies(self, find_text, pages=1):
        pass


class AbstractClassJsonSaver(ABC):

    @abstractmethod
    def save_data_hh(self, data):
        pass

    @abstractmethod
    def save_data_sj(self, data):
        pass

    def clear_data(self, path):
        open(path, 'w').close()
