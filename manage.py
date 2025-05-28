from flask.cli import FlaskGroup
from app import create_app, db
from app.models import Customer, Reservation  # Import your models here

app = create_app()
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
