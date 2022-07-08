from http import HTTPStatus

import orjson
from flask import Blueprint, request

from backend import schemas
from backend.repo.vacancies import VacancyRepo

view = Blueprint('vacancies', __name__)

vacancy_repo = VacancyRepo()


@view.get('/')
@view.get('/<path:status>')
def get_all(status: str=''):
    entities = vacancy_repo.get_by_status(status) if status else vacancy_repo.get_all()

    vacancies = [schemas.VacancyShort.from_orm(entity).dict() for entity in entities]

    return orjson.dumps(vacancies), HTTPStatus.OK


@view.get('/<int:uid>')
def get_by_id(uid):
    entity = vacancy_repo.get_by_id(uid)

    vacancy = schemas.Vacancy.from_orm(entity)
    res = vacancy.dict()

    return orjson.dumps(res), HTTPStatus.OK


@view.put('/<int:uid>')
def update_vacancy(uid):
    payload = request.json
    status = payload['status']

    entity = vacancy_repo.update(uid, status)
    new_vacancy = schemas.Vacancy.from_orm(entity)
    res = new_vacancy.dict()

    return orjson.dumps(res), HTTPStatus.OK


@view.post('/')
def add_vacancy():
    payload = request.json
    new_vacancy = schemas.Vacancy(**payload)

    entity = vacancy_repo.add(
        new_vacancy.uid,
        new_vacancy.area,
        new_vacancy.description,
        new_vacancy.employer,
        new_vacancy.name,
        new_vacancy.published_at,
        new_vacancy.requirement,
        new_vacancy.responsibility,
        new_vacancy.salary_from,
        new_vacancy.salary_to,
        new_vacancy.schedule,
        new_vacancy.status,
        new_vacancy.url,
    )

    new_vacancy = schemas.Vacancy.from_orm(entity).dict()

    return orjson.dumps(new_vacancy), HTTPStatus.CREATED


@view.delete('/<uid>')
def delete_vacancy(uid):
    vacancy_repo.delete(uid)
    return {}, HTTPStatus.NO_CONTENT
