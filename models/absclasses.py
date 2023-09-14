from abc import ABC, abstractmethod


class AbstractClassAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def save_data(self):
        pass


class AbstractClassJsonSaver(ABC):

    @abstractmethod
    def save_json(self):
        pass
