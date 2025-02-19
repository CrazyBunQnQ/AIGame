from random import random
from services import event_engine

class EventSystem:
    def __init__(self):
        self._setup_events()

    def _setup_events(self):
        event_engine.register_event('game_tick', self._handle_tick)

    def _handle_tick(self):
        if random() < 0.6:  # 60% chance for normal events
            self._trigger_normal_event()
        if random() < 0.05:  # 5% chance for special events
            self._trigger_special_event()

    def _trigger_normal_event(self):
        rand = random()
        if rand < 0.3:  # 30% chance for treasure chest
            event_engine.trigger_event('treasure_chest')
        elif rand < 0.5:  # 20% chance for materials
            event_engine.trigger_event('material_found')
        else:  # 10% chance for equipment
            event_engine.trigger_event('equipment_found')

        if random() < 0.5:  # 50% chance for monster attack
            event_engine.trigger_event('monster_attack')

        if random() < 0.3:  # 30% chance for weather change
            event_engine.trigger_event('weather_change')

    def _trigger_special_event(self):
        rand = random()
        if rand < 0.5:  # 50% chance for hidden boss
            event_engine.trigger_event('hidden_boss')
        else:  # 50% chance for time rift
            event_engine.trigger_event('time_rift')

# Example event handlers
def on_treasure_chest():
    print("Treasure chest found!")

def on_material_found():
    print("Materials discovered!")

def on_equipment_found():
    print("Equipment obtained!")

def on_monster_attack():
    print("Monster attack!")

def on_weather_change():
    print("Weather changed!")

def on_hidden_boss():
    print("Hidden boss appeared!")

def on_time_rift():
    print("Time rift opened!")

# Register example handlers
event_engine.register_event('treasure_chest', on_treasure_chest)
event_engine.register_event('material_found', on_material_found)
event_engine.register_event('equipment_found', on_equipment_found)
event_engine.register_event('monster_attack', on_monster_attack)
event_engine.register_event('weather_change', on_weather_change)
event_engine.register_event('hidden_boss', on_hidden_boss)
event_engine.register_event('time_rift', on_time_rift)

# Initialize the event system
event_system = EventSystem()