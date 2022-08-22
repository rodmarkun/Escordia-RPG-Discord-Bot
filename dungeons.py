import random
import items
import enemies
import json

class Dungeon:

    def __init__(self, name, enemies, loot_pool, boss, min_enemy_rooms, min_loot_rooms,  max_enemy_rooms, max_loot_rooms, player_name, dungeon_number, recommended_lvl) -> None:
        self.name = name
        self.enemies = enemies
        self.loot_pool = loot_pool
        self.boss = boss
        self.min_enemy_rooms = min_enemy_rooms
        self.min_loot_rooms = min_loot_rooms
        self.max_enemy_rooms = max_enemy_rooms
        self.max_loot_rooms = max_loot_rooms
        self.enemy_rooms = random.randint(min_enemy_rooms, max_enemy_rooms)
        self.loot_rooms = random.randint(min_loot_rooms, max_loot_rooms)
        self.player_name = player_name
        self.dungeon_number = dungeon_number
        self.recommended_lvl = recommended_lvl
    
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

    dungeon = Dungeon(dungeon_json['name'], default_instance.enemies, default_instance.loot_pool,
                      default_instance.boss, default_instance.min_enemy_rooms, default_instance.min_loot_rooms,
                      default_instance.max_enemy_rooms, default_instance.max_loot_rooms, dungeon_json['player_name'],
                      dungeon_json['dungeon_number'], default_instance.recommended_lvl)

    dungeon.enemy_rooms = dungeon_json['enemy_rooms']
    dungeon.loot_rooms = dungeon_json['loot_rooms']
    return dungeon

dungeon_goblins_nest = Dungeon("Goblins Den", enemies.dungeon_1_enemies, items.dungeon_area_1_loot, enemies.GoblinElite, 2, 2, 3, 3, '', 1, 4)
dungeon_enchanted_graveyard = Dungeon("Enchanted Graveyard", enemies.dungeon_2_enemies, items.dungeon_area_2_loot, enemies.SkeletonDragon, 3, 2, 4, 3, '', 2, 8)
dungeon_black_ant_nest = Dungeon("Black Ant Nest", enemies.dungeon_3_enemies, items.dungeon_area_2_loot, enemies.BlackAntQueen, 4, 0, 4, 0, '', 3, 10)

all_dungeons = {1 : dungeon_goblins_nest, 2 : dungeon_enchanted_graveyard, 3 : dungeon_black_ant_nest}