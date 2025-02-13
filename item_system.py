import random

class Item:
    def __init__(self, name, rarity, base_attack, base_defense, level=1):
        self.name = name
        self.rarity = rarity
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.level = level
        
    def calculate_stats(self):
        """根据稀有度计算随机属性"""
        multiplier_ranges = {
            'N': (0.8, 1.2),
            'R': (1.0, 1.5), 
            'SR': (1.2, 1.8),
            'SSR': (1.5, 2.0)
        }
        
        min_mult, max_mult = multiplier_ranges.get(self.rarity, (1.0, 1.0))
        multiplier = random.uniform(min_mult, max_mult)
        
        self.attack = int(self.base_attack * multiplier * self.level)
        self.defense = int(self.base_defense * multiplier * self.level)
        return self.attack, self.defense
        
    def __repr__(self):
        return f"Item({self.name}, {self.rarity}, ATK:{self.attack}, DEF:{self.defense}, Lv.{self.level})"

if __name__ == "__main__":
    # 测试不同稀有度的物品
    rarities = ['N', 'R', 'SR', 'SSR', 'SSR']
    for i, rarity in enumerate(rarities, 1):
        item = Item(
            name=f"测试武器_{i}",
            rarity=rarity,
            base_attack=100,
            base_defense=50,
            level=3
        )
        item.calculate_stats()
        print(f"{rarity}级物品: {item}")