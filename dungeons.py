import random
import items
import enemies
import json

class Dungeon:
    '''
    Class holding all info related to dungeons.
    '''

    def __init__(self, name, enemy_list, loot_pool, boss, min_enemy_rooms, min_loot_rooms,  max_enemy_rooms, max_loot_rooms, player_name, dungeon_number, recommended_lvl) -> None:
        '''
        Creates a new dungeon.

        :param name: Name of the dungeon
        :param enemy_list: List of enemies that will appear in the dungeon
        :param loot_pool: Objects that will appear in the dungeon
        :param boss: Dungeon's boss
        :param min_enemy_rooms: Minimum amount of enemy rooms inside the dungeon
        :param min_loot_rooms: Minimum amount of loot rooms inside the dungeon
        :param max_enemy_rooms: Maximum amount of enemy rooms inside the dungeon
        :param max_loot_rooms: Maximum amount of loot rooms inside the dungeon
        :param player_name: Player which has entered the dungeon
        :param dungeon_number: Number of dungeon (not that relevant)
        :param recommended_lvl: Recommended level for this dungeon. Will be displayed to the player.
        '''

        self.name = name
        self.enemy_list = enemy_list
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
        '''
        Transforms a dungeon instance into a JSON

        :return: JSON data
        '''
        dung_data = {"name" : self.name,
                    "enemy_rooms" : self.enemy_rooms,
                    "loot_rooms" : self.loot_rooms,
                    "player_name" : self.player_name,
                    "dungeon_number" : self.dungeon_number
                    }
        return json.dumps(dung_data)

def createDungeon(dungeon_json):
    '''
    Create a new Dungeon instance from a Dungeon JSON

    :param dungeon_json: JSON containing the Dungeon
    :return: Dungeon instance
    '''
    default_instance = all_dungeons[dungeon_json['dungeon_number']]

    dungeon = Dungeon(dungeon_json['name'], default_instance.enemy_list, default_instance.loot_pool,
                      default_instance.boss, default_instance.min_enemy_rooms, default_instance.min_loot_rooms,
                      default_instance.max_enemy_rooms, default_instance.max_loot_rooms, dungeon_json['player_name'],
                      dungeon_json['dungeon_number'], default_instance.recommended_lvl)

    dungeon.enemy_rooms = dungeon_json['enemy_rooms']
    dungeon.loot_rooms = dungeon_json['loot_rooms']
    return dungeon

'''
///////////////////////////////// Dungeon Instances ////////////////////////////////////
'''

dungeon_goblins_nest = Dungeon("Goblins Den", enemies.dungeon_1_enemies, items.dungeon_area_1_loot, enemies.GoblinElite, 2, 1, 3, 3, '', 1, 4)

dungeon_enchanted_graveyard = Dungeon("Enchanted Graveyard", enemies.dungeon_2_enemies, items.dungeon_area_2_loot, enemies.SkeletonDragon, 3, 2, 3, 3, '', 2, 7)
dungeon_black_ant_nest = Dungeon("Black Ant Nest", enemies.dungeon_3_enemies, items.dungeon_area_3_loot, enemies.BlackAntQueen, 3, 2, 3, 3, '', 3, 9)

'''
///////////////////////////////// List of all Dungeons ////////////////////////////////////
'''
all_dungeons = {1 : dungeon_goblins_nest, 2 : dungeon_enchanted_graveyard, 3 : dungeon_black_ant_nest}