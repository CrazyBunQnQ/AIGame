from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Enum, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://aigame:password@localhost/aigame'
Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    level = Column(Integer, default=1)
    exp = Column(BigInteger, default=0)
    attack = Column(Integer, default=5)
    defense = Column(Integer, default=5)
    last_active = Column(TIMESTAMP)

class Inventory(Base):
    __tablename__ = 'inventory'
    player_id = Column(Integer, primary_key=True)
    item_type = Column(Enum('WEAPON','ARMOR','MATERIAL'))
    rarity = Column(Enum('N','R','SR','SSR'))
    count = Column(Integer)

with app.app_context():
    Base.metadata.create_all(engine)

@app.route('/gacha', methods=['POST'])
def gacha():
    return jsonify({
        'result': random.choices(
            ['N','R','SR','SSR'],
            weights=[70,25,4.9,0.1],
            k=1
        )[0]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53742)
