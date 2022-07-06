from backend.app import create_app
from backend.config import config
from .parser.hh import run_parser


def main():
    app = create_app()
    app.run(
        port=config.server.port,
        host=config.server.host,
        debug=False,
    )

if __name__ == '__main__':
    main()
    run_parser()
