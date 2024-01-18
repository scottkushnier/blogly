"""Flask application for 'flask run': just make the app, defined elsewhere."""

from create_app import create_app
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

app = create_app()
