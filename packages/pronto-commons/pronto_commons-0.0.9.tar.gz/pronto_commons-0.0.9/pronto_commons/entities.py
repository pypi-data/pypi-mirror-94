from dataclasses import dataclass, field


@dataclass
class Point:
    latitude: float
    longitude: float

@dataclass
class PhoneNumber:
    country_code: str
    national_number: str
    international_format: str = field(init=False) 

    def __post_init__(self):
        self.international_format = f"+{self.country_code}{self.national_number}"
