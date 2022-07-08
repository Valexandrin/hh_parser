from pydantic import BaseModel
from datetime import datetime


class Schema(BaseModel):

    class Config:
        orm_mode = True


class Vacancy(Schema):
    uid: int
    area: str
    description: str
    employer: str
    name: str
    published_at: datetime
    requirement: str = None
    responsibility: str = None
    salary_from: str = None
    salary_to: str = None
    schedule: str
    status: str
    url: str


class VacancyShort(Schema):
    uid: int
    area: str
    employer: str
    name: str
    published_at: datetime
    requirement: str = None
    responsibility: str = None
    schedule: str
    status: str
