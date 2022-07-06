from sqlalchemy.exc import IntegrityError

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
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return vacancy
