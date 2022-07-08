from flask import Flask
from http import HTTPStatus

from backend.view import vacancies
from backend.db import db_session
from backend.errors import AppError
from pydantic import ValidationError


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.status


def handle_validation_error(error: ValidationError):
    return error.json(), HTTPStatus.BAD_REQUEST


def shutdown_session(exception=None):
    db_session.remove()


def create_app():
    app = Flask(__name__)

    app.register_blueprint(vacancies.view, url_prefix='/api/v1/vacancies')

    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)

    app.teardown_appcontext(shutdown_session)

    return app
