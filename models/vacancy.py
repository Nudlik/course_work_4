from dataclasses import dataclass, field


@dataclass(frozen=True)
class Vacancy:
    name: str = field(compare=False)
    url: str = field(compare=False)
    salary: int
    experience: str = field(compare=False)
    requirements: str = field(compare=False)
    city: str = field(compare=False)
