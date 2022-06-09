from sqlalchemy import Column, Integer, String, Date

from backend.db import Base, engine


class Vacancy(Base):
    __tablename__ = 'vacancies'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    area = Column(String, nullable=False)
    salary_from = Column(String)
    salary_to = Column(String)
    published_at = Column(Date, nullable=False)
    url = Column(String)
    employer = Column(String)
    requirement = Column(String)
    responsibility = Column(String)
    schedule = Column(String)


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    main()
