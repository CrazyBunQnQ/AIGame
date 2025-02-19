import random
from typing import List, Dict

class GachaSystem:
    def __init__(self):
        self.rarity_rates = {
            'N': 70,
            'R': 25,
            'SR': 4.9,
            'SSR': 0.1
        }
        
        self.fusion_success_rate = 0.3  # 30% success rate for fusion
        self.luck_factor = 1000  # Used in fusion success calculation

    def single_pull(self) -> str:
        """Perform a single gacha pull"""
        return random.choices(
            list(self.rarity_rates.keys()),
            weights=list(self.rarity_rates.values()),
            k=1
        )[0]

    def multi_pull(self, count: int) -> List[str]:
        """Perform multiple gacha pulls"""
        return random.choices(
            list(self.rarity_rates.keys()),
            weights=list(self.rarity_rates.values()),
            k=count
        )

    def calculate_fusion_success(self, luck: int) -> float:
        """Calculate fusion success rate based on luck"""
        return min(self.fusion_success_rate * (1 + luck / self.luck_factor), 0.9)

    def fuse_items(self, items: List[str], luck: int) -> Dict[str, str]:
        """Attempt to fuse items into a higher rarity"""
        if len(items) != 3:
            raise ValueError("Exactly 3 items are required for fusion")
            
        if not all(item == 'SR' for item in items):
            raise ValueError("All items must be SR rarity for fusion")
            
        success_rate = self.calculate_fusion_success(luck)
        success = random.random() < success_rate
        
        return {
            'success': success,
            'result': 'SSR' if success else 'SR'
        }