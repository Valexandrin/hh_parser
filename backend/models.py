from sqlalchemy import Column, Integer, String, Date

from backend.db import Base, engine


class Vacancy(Base):
    __tablename__ = 'vacancies'

    uid = Column(Integer, primary_key=True)
    area = Column(String, nullable=False)
    description = Column(String)
    employer = Column(String)
    name = Column(String, nullable=False)
    published_at = Column(Date, nullable=False)
    requirement = Column(String)
    responsibility = Column(String)
    salary_from = Column(String)
    salary_to = Column(String)
    schedule = Column(String)
    status = Column(String, nullable=False, default='new')
    url = Column(String)


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    main()
