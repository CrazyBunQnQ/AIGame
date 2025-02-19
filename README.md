# AIGame - 概率元素挂机游戏后端服务

## 环境准备

在开始之前，请确保已安装以下依赖：

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 MySQL 客户端
sudo apt-get update
sudo apt-get install -y default-mysql-client

# 创建 .env 文件并配置数据库连接信息
# 示例 .env 文件内容：
# DB_USER=your_database_user
# DB_PASSWORD=your_database_password
# DB_HOST=your_database_host
# DB_PORT=your_database_port
# DB_NAME=your_database_name
```
```

## 概述
基于Python+MySQL开发的挂机游戏后端服务，融合随机事件、概率战斗、抽卡合成等机制，提供丰富的概率驱动玩法。

## 核心功能

### 1. 随机事件系统
- 🎲 普通事件（60%触发概率）
  - 宝箱发现（30%获得金币/20%获得材料/10%装备）
  - 怪物袭击（战斗胜利率=攻击/(攻击+怪物防御)）
  - 天气变化（影响资源获取概率±15%）
- 🌟 特殊事件（5%触发概率）
  - 隐藏BOSS（掉落SSR装备概率0.1%）
  - 时空裂隙（限时任务完成奖励×3）

### 2. 角色成长系统
- 📈 属性随机成长（升级时攻击/防御/速度+1~3）
- 🛡️ 装备掉落分级（N/R/SR/SSR 概率 70%/25%/4%/1%）
- 🔄 概率突破机制（+10强化成功率50%并逐级递减）

### 3. 自动战斗系统
- ⚔️ 战斗公式：`胜率 = (攻击²)/(攻击² + 敌方防御²) ± 10%随机浮动`
- 🤖 自动巡逻（每小时触发3-5次随机遭遇）
- 👥 PvP遭遇（在线玩家匹配概率：同等级段20%）

### 4. 抽卡合成系统
- 🃏 卡池概率配置：
  ```json
  {
    "N": 70,
    "R": 25, 
    "SR": 4.9,
    "SSR": 0.1
  }
  ```
- 🔥 熔炉系统（3件SR=30%概率合成SSR）
- 🧪 合成公式：`合成成功率 = min(30% × (1 + 幸运值/1000), 90%)`

### 5. 经济系统
- 💰 离线收益公式：`基础值 × (1 + VIP等级×0.2) × 随机系数(0.8-1.2)`
- 📈 市场波动（每小时价格变化±5%）

## 事件系统

### Event Engine 设计

事件引擎提供了一个灵活的事件驱动架构，允许在游戏的不同模块之间进行解耦通信。主要功能包括：

1. **事件注册**
   ```python
   event_engine.register_event(event_name, callback)
   ```
   注册一个事件监听器，当指定事件触发时执行回调函数

2. **事件触发**
   ```python
   event_engine.trigger_event(event_name, *args, **kwargs)
   ```
   触发指定事件，并传递任意参数给注册的回调函数

3. **事件移除**
   ```python
   event_engine.remove_event(event_name, callback=None)
   ```
   移除指定事件的监听器，如果未指定callback则移除该事件的所有监听器

### 使用示例

```python
from services import event_engine

# 注册事件
def on_player_login(player):
    print(f"Player logged in: {player.name}")
event_engine.register_event('player_login', on_player_login)

# 触发事件
event_engine.trigger_event('player_login', current_player)

# 移除事件
event_engine.remove_event('player_login', on_player_login)
```

## 技术架构
- Python 3.10+
- Flask框架
- MySQL 8.0+
- SQLAlchemy ORM

## 数据库设计
```sql
CREATE DATABASE aigame;
CREATE TABLE players (
    id INT PRIMARY KEY AUTO_INCREMENT,
    level INT DEFAULT 1,
    exp BIGINT DEFAULT 0,
    attack INT DEFAULT 5,
    defense INT DEFAULT 5,
    last_active TIMESTAMP
);

CREATE TABLE inventory (
    player_id INT,
    item_type ENUM('WEAPON','ARMOR','MATERIAL'),
    rarity ENUM('N','R','SR','SSR'),
    count INT,
    FOREIGN KEY (player_id) REFERENCES players(id)
);
```

## 快速开始
1. 启动服务：
```python
FLASK_APP=main.py flask run --host=0.0.0.0 --port=53742
```

## API示例
```python
@app.route('/gacha', methods=['POST'])
def gacha():
    # 抽卡逻辑实现
    return jsonify({
        'result': random.choices(
            ['N','R','SR','SSR'], 
            weights=[70,25,4.9,0.1], 
            k=1
        )[0]
    })
```