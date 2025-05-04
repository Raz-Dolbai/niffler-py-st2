from dataclasses import dataclass
from faker import Faker

fake = Faker()


@dataclass
class Category:
    SCHOOL = "school"
    CAR = "car"
    TEXT_2_CHARACTERS = "".join(fake.random_letters(length=2))
    TEXT_3_CHARACTERS = "".join(fake.random_letters(length=3))
    TEXT_50_ELEMENTS = "".join(fake.random_letters(length=50))
    TEXT_49_ELEMENTS = "".join(fake.random_letters(length=49))
    TEXT_51_ELEMENTS = "".join(fake.random_letters(length=51))
    TEXT_101_ELEMENTS = "".join(fake.random_letters(length=101))
    TEXT_100_ELEMENTS = "".join(fake.random_letters(length=101))
    TEXT_99_ELEMENTS = "".join(fake.random_letters(length=101))

