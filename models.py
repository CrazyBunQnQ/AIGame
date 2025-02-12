from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.BigInteger, default=0)
    gold = db.Column(db.BigInteger, default=0)
    attack = db.Column(db.Integer, default=10)
    defense = db.Column(db.Integer, default=10)
    speed = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    items = db.relationship('Item', backref='player', lazy=True)
    events = db.relationship('Event', backref='player', lazy=True)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    name = db.Column(db.String(255), nullable=False)
    rarity = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    stats = db.Column(db.JSON)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    type = db.Column(db.String(50), nullable=False)
    outcome = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
