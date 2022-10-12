from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:password123@127.0.0.1:5432/trello'

db = SQLAlchemy(app)

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)

#defining a custom cli (terminal) command
@app.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created successfully!')

@app.cli.command('seed')
def seed():
    card = Card(
        title = 'Start the project',
        description = 'Stage 1 - Creating the database',
        status = 'To-do',
        priority = 'High',
        date = date.today()
    )

    db.session.add(card)
    db.session.commit()
    print('Tables seeded successfully!')

@app.cli.command('drop')
def drop():
    db.drop_all()
    print('Tables dropped successfully!')
    
@app.route('/')
def index():
    return 'Hello World'


