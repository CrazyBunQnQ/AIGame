import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS players 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             username TEXT UNIQUE, 
             level INTEGER DEFAULT 1, 
             experience INTEGER DEFAULT 0, 
             gold INTEGER DEFAULT 0, 
             attack INTEGER DEFAULT 10, 
             defense INTEGER DEFAULT 10, 
             speed INTEGER DEFAULT 10, 
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS items 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             player_id INTEGER, 
             name TEXT, 
             rarity TEXT CHECK(rarity IN ('common', 'rare', 'epic', 'legendary')), 
             type TEXT CHECK(type IN ('weapon', 'armor', 'accessory')), 
             stats TEXT, 
             FOREIGN KEY(player_id) REFERENCES players(id))''')
c.execute('''CREATE TABLE IF NOT EXISTS events 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             player_id INTEGER, 
             type TEXT CHECK(type IN ('treasure', 'monster', 'weather', 'special')), 
             outcome TEXT, 
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
             FOREIGN KEY(player_id) REFERENCES players(id))''')
conn.commit()
conn.close()
