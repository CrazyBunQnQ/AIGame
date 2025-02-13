from datetime import datetime
from flask import request, jsonify
from app import app
from models import Player, Item, Event
import random
from datetime import datetime, timedelta

@app.route('/player', methods=['POST'])
def create_player():
    data = request.json
    new_player = Player(
        username=data['username'],
        vip_level=data.get('vip_level', 0),
        luck=data.get('luck', 0),
        attack=data.get('attack', 10),
        defense=data.get('defense', 10),
        speed=data.get('speed', 10)
    )
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
    
    # 触发随机事件
    event_result = handle_random_events(player)
    
    # 计算离线收益（示例实现）
    offline_minutes = (datetime.utcnow() - player.last_active).total_seconds() // 60
    vip_multiplier = 1 + player.vip_level * 0.2
    base_gold = 10 * offline_minutes
    gold_gained = int(base_gold * vip_multiplier * random.uniform(0.8, 1.2))
    
    # 更新玩家数据
    player.gold += gold_gained
    player.last_active = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'event': event_result,
        'gold_gained': gold_gained,
        'new_gold': player.gold
    })

@app.route('/gacha', methods=['POST'])
def gacha():
    """抽卡接口实现"""
    result = random.choices(
        ['N', 'R', 'SR', 'SSR'],
        weights=[70, 25, 4.9, 0.1],
        k=1
    )[0]
    
    if 'player_id' in request.json:
        item = Item(
            player_id=request.json['player_id'],
            item_type='CARD',
            rarity=result,
            count=1
        )
        db.session.add(item)
        db.session.commit()
    
    return jsonify({'result': result})

@app.route('/combine', methods=['POST'])
def combine_items():
    """装备合成接口"""
    player_id = request.json['player_id']
    items = Item.query.filter(
        Item.player_id == player_id,
        Item.rarity == 'SR'
    ).limit(3).all()
    
    if len(items) < 3:
        return jsonify({'error': '需要3个SR装备'}), 400
    
    for item in items:
        db.session.delete(item)
    
    if random.random() < 0.3:
        new_item = Item(
            player_id=player_id,
            item_type='EQUIPMENT',
            rarity='SSR',
            count=1
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'result': 'success', 'item': 'SSR'})
    
    db.session.commit()
    return jsonify({'result': 'failed'})

def handle_random_events(player):
    rand = random.random()    
    if rand < 0.05:
        return special_events(player)
    elif rand < 0.65:
        return normal_events(player)
    return None

def normal_events(player):
    event_type = random.choices(
        ['treasure', 'monster', 'weather'],
        weights=[0.3, 0.3, 0.4]
    )[0]
    
    if event_type == 'treasure':
        loot = random.choices(
            ['gold', 'material', 'equipment'],
            weights=[30, 20, 10]
        )[0]
        return {'type': 'treasure', 'loot': loot}
    
    elif event_type == 'monster':
        base_rate = (player.attack**2) / (player.attack**2 + 50**2)
        success_rate = base_rate + random.uniform(-0.1, 0.1)
        return {'type': 'battle', 'success_rate': success_rate}
    
    elif event_type == 'weather':
        weather_effect = random.choice(['sunny', 'rainy', 'stormy'])
        return {'type': 'weather', 'effect': weather_effect}

def special_events(player):
    event_type = random.choice(['boss', 'rift'])
    if event_type == 'boss':
        if random.random() < 0.001:
            return {'type': 'boss', 'result': 'SSR obtained'}
        return {'type': 'boss', 'result': 'no loot'}
    elif event_type == 'rift':
        return {'type': 'rift', 'bonus': '3x rewards'}
