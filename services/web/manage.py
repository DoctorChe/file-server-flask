from flask.cli import FlaskGroup

from project import db
from project.app import app
from project.models import User


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
    print("Created database")


@cli.command("seed_db")
def seed_db():
    with app.app_context():
        user = User(name=app.config["ADMIN_LOGIN"])
        user.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(user)
        user = User(name=app.config["USER_LOGIN"])
        user.set_password(app.config["USER_PASSWORD"])
        db.session.add(user)
        db.session.commit()
    print("Seeded database")


if __name__ == "__main__":
    cli()
