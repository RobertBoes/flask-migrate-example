from random import randint

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

        for product_number in range(1, randint(2, 6)):
            quantity = randint(1, 3)
            order = Order(
                quantity=quantity,
                item='Product #{product_number}'.format(product_number=product_number),
                price=quantity*5,
            )
            user.orders.append(order)

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


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    item = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)


class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order

    id = ma.auto_field()
    quantity = ma.auto_field()
    item = ma.auto_field()
    price = ma.auto_field()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    orders = ma.List(ma.Nested(OrderSchema))


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def index():
    return users_schema.jsonify(User.query.all())
