# flask-migrate-example

This is an example project that uses [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) to handle migrations. 

## Setup

1. **Create a virtual environment**\
`python3 -m venv venv`

2. **Activate the virtual environment**\
Linux/Mac: `source ./venv/bin/activate`\
Windows: `venv\Scripts\Activate.bat` or `venv\Scripts\Activate.ps1`

3. **Installing requirements**\
`pip install -r requirements.txt`

4. **Configure app**\
Firstly, create an empty mysql scheme and user that has access to that scheme on your local machine.\
Update the `.env` configuration to your settings, you can copy the example file by running:\
Linux/Mac: `cp .env.example .env`\
Windows: `copy .env.example .env`

5. **Migrate the database**\
`flask db upgrade` runs all the migrations and creates thus creates the _user_ and _order_ table.

6. **Seeding the database**\
I've added a command to seeds some basic data to the database by calling `flask seed-db`. This will populate the tables with a few rows of data.

7. **Running the flask app**\
`flask run`\
The [index page](http://127.0.0.1:5000/) now outputs JSON of all users + orders.

## Diving deeper

The `migrations` folder contains generated files and the migrations. To setup in a new project you'd run `flask db init` to generate the base config files and template.

`flask db migrate -m "My migration name"` generates a new migration. However, a migration will only be generated when the models and connected database **don't** match.

We can test this by adding a new model with a relation to that model in `app.py`:

```diff
+ class BillingMethod(db.Model):
+     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
+     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
+     credit_card = db.Column(db.String(128), nullable=False)


  class User(db.Model):
      id = db.Column(db.Integer, primary_key=True, autoincrement=True)
      name = db.Column(db.String(128), nullable=False)
      orders = db.relationship('Order', backref='user', lazy=True)
+     billing_methods = db.relationship('BillingMethod', backref='user', lazy=True)
```

After adding the code above you can generate a migration using `flask db migrate -m "Add billing method"`,
this will generate a file like `/migrations/versions/1d0ec0c0199b_add_billing_method.py`.
Here you can adjust the migration, or add code to transform some data (like in `/migrations/versions/edd9dbc319fe_add_price_to_orders.py`)

To run the migration and update your database, use `flask db upgrade`.
