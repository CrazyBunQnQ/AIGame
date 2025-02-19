import random
from typing import Dict, Tuple

class BattleSystem:
    def __init__(self):
        self.pvp_match_rate = 0.2  # 20% chance for PvP match
        self.random_fluctuation = 0.1  # ±10% random fluctuation in battle

    def calculate_battle_outcome(self, attack: int, defense: int) -> bool:
        """
        Calculate battle outcome using formula:
        win_rate = (attack²)/(attack² + defense²) ± 10% random fluctuation
        """
        base_win_rate = (attack ** 2) / (attack ** 2 + defense ** 2)
        fluctuation = random.uniform(-self.random_fluctuation, self.random_fluctuation)
        final_win_rate = min(max(base_win_rate + fluctuation, 0), 1)
        return random.random() < final_win_rate

    def patrol_encounter(self) -> int:
        """Simulate patrol encounter (3-5 random encounters per hour)"""
        return random.randint(3, 5)

    def pvp_match(self, player_level: int, opponent_level: int) -> bool:
        """
        Simulate PvP match with 20% chance for same level range
        Returns True if PvP match occurs, False otherwise
        """
        if abs(player_level - opponent_level) <= 5:  # Same level range
            return random.random() < self.pvp_match_rate
        return False

    def simulate_battle(self, player_stats: Dict, enemy_stats: Dict) -> Dict:
        """
        Simulate a complete battle with outcome and damage calculation
        """
        player_attack = player_stats['attack']
        player_defense = player_stats['defense']
        
        enemy_attack = enemy_stats['attack']
        enemy_defense = enemy_stats['defense']
        
        player_wins = self.calculate_battle_outcome(player_attack, enemy_defense)
        enemy_wins = self.calculate_battle_outcome(enemy_attack, player_defense)
        
        return {
            'player_wins': player_wins,
            'enemy_wins': enemy_wins,
            'player_damage': enemy_attack - player_defense if enemy_wins else 0,
            'enemy_damage': player_attack - enemy_defense if player_wins else 0
        }