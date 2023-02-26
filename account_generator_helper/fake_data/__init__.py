from dataclasses import dataclass
from typing import List

import requests
from .exceptions import ProblemWithGetPersonData
from .const import Gender


@dataclass
class Name:
    title: str
    first: str
    last: str


@dataclass
class Street:
    number: int
    name: str


@dataclass
class Coordinates:
    latitude: str
    longitude: str


@dataclass
class Timezone:
    offset: str
    description: str


@dataclass
class Location:
    street: Street
    city: str
    state: str
    country: str
    postcode: int
    coordinates: Coordinates
    timezone: Timezone


@dataclass
class Login:
    uuid: str
    username: str
    password: str
    salt: str
    md5: str
    sha1: str
    sha256: str


@dataclass
class Dob:
    date: str
    age: int


@dataclass
class Picture:
    large: str
    medium: str
    thumbnail: str


@dataclass
class Person:
    gender: str
    name: Name
    location: Location
    email: str
    login: Login
    dob: Dob
    phone: str
    picture: Picture
    nat: str


def __get_person(user_data: dict):
    return Person(
        gender=user_data["gender"],
        name=Name(title=user_data["name"]["title"], first=user_data["name"]["first"], last=user_data["name"]["last"]),
        location=Location(
            street=Street(number=user_data["location"]["street"]["number"],
                          name=user_data["location"]["street"]["name"]),
            city=user_data["location"]["city"],
            state=user_data["location"]["state"],
            country=user_data["location"]["country"],
            postcode=user_data["location"]["postcode"],
            coordinates=Coordinates(latitude=user_data["location"]["coordinates"]["latitude"],
                                    longitude=user_data["location"]["coordinates"]["longitude"]),
            timezone=Timezone(offset=user_data["location"]["timezone"]["offset"],
                              description=user_data["location"]["timezone"]["description"])
        ),
        email=user_data["email"],
        login=Login(
            uuid=user_data["login"]["uuid"],
            username=user_data["login"]["username"],
            password=user_data["login"]["password"],
            salt=user_data["login"]["salt"],
            md5=user_data["login"]["md5"],
            sha1=user_data["login"]["sha1"],
            sha256=user_data["login"]["sha256"]
        ),
        dob=Dob(date=user_data["dob"]["date"], age=user_data["dob"]["age"]),
        phone=user_data["phone"],
        picture=Picture(large=user_data["picture"]["large"], medium=user_data["picture"]["medium"],
                        thumbnail=user_data["picture"]["thumbnail"]),
        nat=user_data["nat"])


def generate_person(gender: Gender = Gender.BOTH) -> Person:
    """
    Generate person.

    :param gender: Gender of random person

    :return: Random person
    """
    return generate_persons(1, gender)[0]


def generate_persons(count: int, gender: Gender = Gender.BOTH) -> List[Person]:
    """
    Batch generate persons.

    :param gender: Gender of random person
    :param count: Count of persons to generate

    :return: Random persons
    """
    if not isinstance(count, int) or count < 1:
        count = 1

    r = requests.get('https://randomuser.me/api', params={'gender': gender.value, 'results': count})
    if r.status_code != 200:
        raise ProblemWithGetPersonData()

    return [__get_person(data) for data in r.json()['results']]
