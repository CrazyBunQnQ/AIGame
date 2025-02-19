from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

import os
from dotenv import load_dotenv
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def index():
    return 'AIGame backend is running!'

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    new_score = Score(
        player_name=data['player_name'],
        score=data['score']
    )
    db.session.add(new_score)
    db.session.commit()
    return jsonify({'message': 'Score submitted successfully'}), 201

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    scores = Score.query.order_by(Score.score.desc()).limit(10).all()
    return jsonify([{
        'player_name': score.player_name,
        'score': score.score,
        'timestamp': score.created_at
    } for score in scores])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51926)