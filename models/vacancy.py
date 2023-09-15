from dataclasses import dataclass, field


@dataclass(frozen=True)
class Vacancy:
    name: str = field(compare=False)
    url: str = field(compare=False)
    salary: int
    experience: str = field(compare=False)
    requirements: str = field(compare=False)
    city: str = field(compare=False)

    def __str__(self):
        return f'Вакансия:              {self.name}\n' \
               f'Ссылка:                {self.url}\n' \
               f'Зарплатные ожидания:   {self.salary}\n' \
               f'Опыт работы:           {self.experience}\n' \
               f'Требования/информация: {self.requirements}\n' \
               f'Город:                 {self.city}'
