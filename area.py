import enemies
import dungeons

class Area:
    def __init__(self, name, number, enemyList, boss, dungeons):
        self.name = name
        self.number = number
        self.enemyList = enemyList
        self.boss = boss
        self.dungeons = dungeons

    def show_info(self):
        return f'You are currently in **{self.name}** (area {self.number})\n'

area_1 = Area("Quiet Woods", 1, enemies.area_1_enemies, enemies.area_1_boss, [dungeons.dungeon_globlins_nest])
areas = [area_1]