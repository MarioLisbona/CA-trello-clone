from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:password123@127.0.0.1:5432/trello'

db = SQLAlchemy(app)

#create the Card Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class CardSchema(ma.Schema):
    class Meta:
        #fields to expose
        fields = ('id', 'title', 'description', 'date', 'status', 'priority')
    
#single card schema when a single card is retrieved
card_schema = CardSchema()

#multiple card schema, when many cards need to be retrieved
cards_schema = CardSchema(many=True)


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
    card1 = Card(
        title = 'Start the project',
        description = 'Stage 1 - Creating the database',
        status = 'To-do',
        priority = 'High',
        date = date.today()
    )

    card2 = Card(
        title = 'Select vintal features',
        description = 'Stage 2 - Creating the front end',
        status = 'To-do',
        priority = 'Medium',
        date = date.today()
    )

    card3 = Card(
        title = 'Start the project',
        description = 'Stage 3 - coding the backend',
        status = 'To-do',
        priority = 'Low',
        date = date.today()
    )

    db.session.add(card1)
    db.session.add(card2)
    db.session.add(card3)
    db.session.commit()
    print('Tables seeded successfully!')

@app.cli.command('drop')
def drop():
    db.drop_all()
    print('Tables dropped successfully!')
    
@app.route('/')
def index():
    return 'Hello World'

@app.route('/cards/', methods=['GET'])
def get_cards():
    #retrieve all the cards from the database table 'cards'
    cards_list = Card.query.all()

    #Convert the cards from the database into a JSON format and store them in result
    result = cards_schema.dump(cards_list)

    #return the data in json format
    return jsonify(result)

