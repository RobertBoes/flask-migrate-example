from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, downgrade
import config

app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI'] = '{driver}://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(
    driver=app.config['DB_DRIVER'],
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    host=app.config['DB_HOST'],
    port=app.config['DB_PORT'],
    database=app.config['DB_NAME'],
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


@app.cli.command("seed-db")
def seed():
    """Seed the database."""
    seed_db()


def seed_db():
    for number in range(1, 10):
        user = User(name='Test user {number}'.format(number=number))
        db.session.add(user)
        db.session.flush()
    db.session.commit()


@app.cli.command("reset-db")
def reset_db():
    print('Dropping all tables (flask db downgrade base)')
    downgrade(revision='base')
    print('')
    print('Upgrading (flask db upgrade)')
    upgrade()
    print('')
    print('Seeding (flask seed)')
    seed_db()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def index():
    return users_schema.jsonify(User.query.all())
