from flask.cli import FlaskGroup

from project.app import app, db, User


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


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


if __name__ == "__main__":
    cli()
