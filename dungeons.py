import random
import items
import enemies
import json

class Dungeon():

    def __init__(self, name, enemies, loot_pool, boss, max_enemy_rooms, max_loot_rooms, player_name, dungeon_number) -> None:
        self.name = name
        self.enemies = enemies
        self.loot_pool = loot_pool
        self.boss = boss
        self.max_enemy_rooms = max_enemy_rooms
        self.max_loot_rooms = max_loot_rooms
        self.enemy_rooms = random.randint(round(max_enemy_rooms / 2), max_enemy_rooms)
        self.loot_rooms = random.randint(round(max_loot_rooms / 2), max_loot_rooms)
        self.player_name = player_name
        self.dungeon_number = dungeon_number
    
    def toJSON(self):
        
        dung_data = {"name" : self.name,
                    "enemy_rooms" : self.enemy_rooms,
                    "loot_rooms" : self.loot_rooms,
                    "player_name" : self.player_name,
                    "dungeon_number" : self.dungeon_number
                    }
        return json.dumps(dung_data)

def createDungeon(dungeon_json):
    default_instance = all_dungeons[dungeon_json['dungeon_number']]
    dungeon = Dungeon(dungeon_json['name'], default_instance.enemies, default_instance.loot_pool, default_instance.boss, default_instance.max_enemy_rooms, default_instance.max_loot_rooms, dungeon_json['player_name'], dungeon_json['dungeon_number'])
    dungeon.enemy_rooms = dungeon_json['enemy_rooms']
    dungeon.loot_rooms = dungeon_json['loot_rooms']

    return dungeon

dungeon_globlins_nest = Dungeon("Globins Den", enemies.dungeon_1_enemies, items.dungeon_area_1_loot, enemies.GoblinElite, 3, 3, '', 1)

all_dungeons = {1 : dungeon_globlins_nest}