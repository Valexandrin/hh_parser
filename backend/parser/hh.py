import requests
import json
from backend.models import Vacancy
from backend.db import db_session


def get_vacancies(page=1, date=None):
    params = {
            'text': 'NAME:Python (разработчик OR developer OR программист) NOT (full-stack OR fullstack OR middle OR senior), удаленная работа',
            'date_from': date,
            'page': page, # Индекс страницы поиска на HH
            'per_page': 100 # Кол-во вакансий на 1 странице
        }

    response = requests.get('https://api.hh.ru/vacancies', params)
    data = response.content.decode()
    data = json.loads(data)

    return data


def save_vacancy(vacancy):
    new_vacancy = Vacancy(
                uid = vacancy['id'],
                name = vacancy['name'],
                area = vacancy['area']['name'],
                published_at = vacancy['published_at'],
                url = vacancy['alternate_url'],
                employer = vacancy['employer']['name'],
                requirement = vacancy['snippet']['requirement'],
                responsibility = vacancy['snippet']['responsibility'],
                schedule = vacancy['schedule']['name'],
            )

    if vacancy['salary']:
        if vacancy['salary']['from']:
            new_vacancy.salary_from = vacancy['salary']['from']
        if vacancy['salary']['to']:
            new_vacancy.salary_to = vacancy['salary']['to']

    db_session.add(new_vacancy)
    db_session.commit()


last_update = Vacancy.query.order_by(Vacancy.published_at.desc()).first()
if last_update:
    last_update = last_update.published_at

pages = get_vacancies(date=last_update)['pages']
for page in range(pages):
    vacancies = get_vacancies(page, last_update)['items']

    for vacancy in vacancies:
        exist_vacancy = Vacancy.query.filter(Vacancy.uid==vacancy['id']).count()
        if not exist_vacancy:
            save_vacancy(vacancy)
