import time
import requests
import json
from backend.models import Vacancy
from backend.db import db_session


def get_vacancies(page=1):
    params = {
            'text': 'NAME:Python (разработчик OR developer OR программист) NOT (full-stack OR fullstack OR middle OR senior), удаленная работа',
            'page': page, # Индекс страницы поиска на HH
            'per_page': 100 # Кол-во вакансий на 1 странице
        }

    response = requests.get('https://api.hh.ru/vacancies', params)

    return data_processing(response)


def get_description(vacancy_id):
    response = requests.get('https://api.hh.ru/vacancies/{v_id}'.format(v_id = vacancy_id))

    vacancy = data_processing(response)
    return vacancy['description']


def data_processing(input_data):
    data = input_data.content.decode()
    return json.loads(data)


def save_vacancy(vacancy):
    new_vacancy = Vacancy(
                uid = vacancy['id'],
                area = vacancy['area']['name'],
                description = vacancy['description'],
                employer = vacancy['employer']['name'],
                name = vacancy['name'],
                published_at = vacancy['published_at'],
                requirement = vacancy['snippet']['requirement'],
                responsibility = vacancy['snippet']['responsibility'],
                schedule = vacancy['schedule']['name'],
                status = 'new',
                url = vacancy['alternate_url'],
            )

    if vacancy['salary']:
        if vacancy['salary']['from']:
            new_vacancy.salary_from = vacancy['salary']['from']
        if vacancy['salary']['to']:
            new_vacancy.salary_to = vacancy['salary']['to']

    db_session.add(new_vacancy)
    db_session.commit()


def db_update():
    id_list = []
    pages = get_vacancies()['pages']
    for page in range(pages):
        vacancies = get_vacancies(page)['items']
        for vacancy in vacancies:
            exist_vacancy = Vacancy.query.filter(Vacancy.uid==vacancy['id']).count()
            if not exist_vacancy:
                vacancy['description'] = get_description(vacancy['id'])

                save_vacancy(vacancy)

            id_list.append(int(vacancy['id']))

    db_clean(id_list)


def db_clean(actual_ids: list):
    exist_vacancies = Vacancy.query.all()
    for vacancy in exist_vacancies:
        if vacancy.uid not in actual_ids:
            db_session.delete(vacancy)
            db_session.commit()


def run_parser():
    while True:
        db_update()
        time.sleep(10)


if __name__ == '__main__':
    run_parser()
