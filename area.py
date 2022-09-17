import enemies
import dungeons

class Area:
    '''
    Class containing info of all areas inside the game.
    '''
    def __init__(self, name, number, enemyList, boss, dungeons):
        '''
        Creates a new area.

        :param name: Name of the area
        :param number: Area number (like an ID)
        :param enemyList: Enemies that will appear in this area
        :param boss: Boss of this area
        :param dungeons: Dungeons inside this area
        '''
        self.name = name
        self.number = number
        self.enemyList = enemyList
        self.boss = boss
        self.dungeons = dungeons

    def show_info(self):
        '''
        Shows current area

        :return: Info string
        '''
        return f'You are currently in **{self.name}** (area {self.number})\n'

def show_areas():
    '''
    Shows all areas in the game
    :return: Areas info string
    '''
    areas_txt = ""
    i = 1
    for a in areas:
        areas_txt += f'{i} - {a.name}\n'
        i += 1
    return areas_txt

'''
///////////////////////////////// Area Instances ////////////////////////////////////
'''
area_1 = Area("Quiet Woods", 1, enemies.area_1_enemies, enemies.area_1_boss, [dungeons.dungeon_goblins_nest])
area_2 = Area("Dangerous Crossroads", 2, enemies.area_2_enemies, enemies.area_2_boss, [dungeons.dungeon_enchanted_graveyard, dungeons.dungeon_black_ant_nest])
area_3 = Area("Sacred Lake", 3, enemies.area_3_enemies, enemies.area_3_boss, [])

'''
///////////////////////////////// All areas inside the game ////////////////////////////////////
'''
areas = [area_1, area_2, area_3]