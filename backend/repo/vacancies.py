from backend.models import Vacancy
from backend.errors import NotFoundError, ConflictError

from sqlalchemy.exc import IntegrityError

class VacancyRepo:
    name = 'vacancy'

    def get_all(self) -> list[Vacancy]:
        return Vacancy.query.all()

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

        return vacancy
