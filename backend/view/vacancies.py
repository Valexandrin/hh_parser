from http import HTTPStatus

from flask import Blueprint, jsonify, request

from backend import schemas
from backend.repo.vacancies import VacancyRepo

view = Blueprint('vacancies', __name__)

vacancy_repo = VacancyRepo()

@view.get('/')
def get_all():
    entities = vacancy_repo.get_all()
    vacancies = [schemas.Vacancy.from_orm(entity).dict() for entity in entities]
    return jsonify(vacancies), HTTPStatus.OK


@view.get('/<uid>')
def get_by_id(uid):
    entity = vacancy_repo.get_by_id(uid)
    vacancy = schemas.Vacancy.from_orm(entity)
    return vacancy.dict(), HTTPStatus.OK


@view.put('/<uid>')
def update_vacancy(uid):
    payload = request.json
    status = payload['status']

    entity = vacancy_repo.update(uid, status)

    new_vacancy = schemas.Vacancy.from_orm(entity)
    return new_vacancy.dict(), HTTPStatus.OK
