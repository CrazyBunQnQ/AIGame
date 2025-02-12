from flask import request, jsonify
from app import app
from models import Player, Item, Event
import random
from datetime import datetime, timedelta

@app.route('/player', methods=['POST'])
def create_player():
    data = request.json
    new_player = Player(username=data['username'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify({'message': 'Player created', 'player_id': new_player.id}), 201

@app.route('/player/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get_or_404(player_id)
    return jsonify({
        'id': player.id,
        'username': player.username,
        'level': player.level,
        'experience': player.experience,
        'gold': player.gold,
        'stats': {
            'attack': player.attack,
            'defense': player.defense,
            'speed': player.speed
        }
    })

@app.route('/player/<int:player_id>/idle', methods=['POST'])
def idle(player_id):
    player = Player.query.get_or_404(player_id)
    # Basic idle logic - will expand in services.py
    experience_gained = random.randint(10, 50)
    gold_gained = random.randint(5, 20)
    player.experience += experience_gained
    player.gold += gold_gained
    db.session.commit()
    return jsonify({
        'experience_gained': experience_gained,
        'gold_gained': gold_gained,
        'new_experience': player.experience,
        'new_gold': player.gold
    })
