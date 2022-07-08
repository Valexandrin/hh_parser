from sqlalchemy.exc import IntegrityError

from datetime import datetime

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Vacancy


class VacancyRepo:
    name = 'vacancy'

    def get_all(self) -> list[Vacancy]:
        return Vacancy.query.order_by(Vacancy.published_at.desc()).all()

    def get_by_status(self, status: str) -> list[Vacancy]:
        return Vacancy.query.filter(
            Vacancy.status == status).order_by(Vacancy.published_at.desc()).all()

    def get_by_id(self, uid: int) -> Vacancy:
        vacancy = Vacancy.query.filter(Vacancy.uid == uid).first()
        if not vacancy:
            raise NotFoundError(self.name)

        return vacancy

    def update(self, uid: int, status: str) -> Vacancy:
        vacancy = Vacancy.query.filter(Vacancy.uid == uid).first()
        if not vacancy:
            raise NotFoundError(self.name)

        try:
            vacancy.status = status
        except IntegrityError:
            raise ConflictError(self.name)

        db_session.commit()

        return vacancy

    def add(self,
        uid: int,
        area: str,
        description: str,
        employer: str,
        name: str,
        published_at: datetime,
        requirement: str,
        responsibility: str,
        salary_from: str,
        salary_to: str,
        schedule: str,
        status: str,
        url: str,
    ) -> Vacancy:
        try:
            new_vacancy = Vacancy(
                uid = uid,
                area = area,
                description = description,
                employer = employer,
                name = name,
                published_at = published_at,
                requirement = requirement,
                responsibility = responsibility,
                salary_from = salary_from,
                salary_to = salary_to,
                schedule = schedule,
                status = status,
                url = url,
            )
        except IntegrityError:
            raise ConflictError(self.name)

        db_session.add(new_vacancy)
        db_session.commit()

        return new_vacancy

    def delete(self, uid: int) -> None:
        vacancy = Vacancy.query.filter(Vacancy.uid == uid).first()
        db_session.delete(vacancy)
        db_session.commit()
