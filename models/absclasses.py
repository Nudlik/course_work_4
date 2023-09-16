from abc import ABC, abstractmethod


class AbstractClassAPI(ABC):

    __url: str

    @abstractmethod
    def get_vacancies(self, parameters: dict) -> list:
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


class AbstractClassMenu(ABC):

    @abstractmethod
    def show_menu(self):
        pass
