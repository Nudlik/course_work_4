from abc import ABC, abstractmethod


class AbstractClassAPI(ABC):

    url: str
    path_to_json: str

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def save_data(self):
        pass

    def clear_data(self):
        open(self.path_to_json, 'w').close()


class AbstractClassJsonSaver(ABC):

    @abstractmethod
    def save_json(self):
        pass
