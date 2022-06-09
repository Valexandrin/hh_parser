import requests
import json
from backend.models import Vacancy
from backend.db import db_session


def get_vacancies():
    params = {
            'text': 'NAME:Python разработчик, удаленная работа',
            'page': 1, # Индекс страницы поиска на HH
            'per_page': 20 # Кол-во вакансий на 1 странице
        }

    response = requests.get('https://api.hh.ru/vacancies', params)
    data = response.content.decode()

    data = json.loads(data)
    vacancies = data['items']

    for vacancy in vacancies:
        new_vacancy = Vacancy(
            uid = vacancy['id'],
            name = vacancy['name'],
            area = vacancy['area']['name'],
            published_at = vacancy['published_at'],
            url = vacancy['url'],
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


get_vacancies()
