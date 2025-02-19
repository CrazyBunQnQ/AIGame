import random
from typing import Dict, Tuple

class CharacterGrowth:
    def __init__(self):
        self.enhancement_success_rates = {
            1: 1.0,
            2: 0.9,
            3: 0.8,
            4: 0.7,
            5: 0.6,
            6: 0.5,
            7: 0.4,
            8: 0.3,
            9: 0.2,
            10: 0.1
        }
        
        self.equipment_drop_rates = {
            'N': 0.7,
            'R': 0.25,
            'SR': 0.049,
            'SSR': 0.001
        }

    def level_up(self, current_stats: Dict[str, int]) -> Dict[str, int]:
        """Randomly increase stats when leveling up"""
        return {
            'attack': current_stats['attack'] + random.randint(1, 3),
            'defense': current_stats['defense'] + random.randint(1, 3),
            'speed': current_stats['speed'] + random.randint(1, 3)
        }

    def get_equipment_drop(self) -> str:
        """Get random equipment based on drop rates"""
        return random.choices(
            list(self.equipment_drop_rates.keys()),
            weights=list(self.equipment_drop_rates.values()),
            k=1
        )[0]

    def enhance_equipment(self, current_level: int) -> Tuple[bool, int]:
        """Attempt to enhance equipment with decreasing success rate"""
        if current_level not in self.enhancement_success_rates:
            return False, current_level
            
        success = random.random() < self.enhancement_success_rates[current_level]
        return success, current_level + 1 if success else current_level