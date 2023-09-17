from dataclasses import dataclass


@dataclass(frozen=True)
class OptionDictParams:
    """ Класс для хранения параметров для парсинга """

    text: str
    salary: int
    city: str
    experience: int
    pages: int
