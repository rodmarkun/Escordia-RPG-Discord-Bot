from random import randint
import combat
import items

'''
Enemy class definitions, specially for custom stats and rewards.
'''

class Enemy(combat.Battler):
    '''
    Base class for all enemies. Inherits class 'Battler'.

    Attributes:
    xpReward : int    
        Amount of xp (Experience Points) given when slain
    goldReward : int 
        Amount of gold (coins/money) given when slain
    '''
    def __init__(self, name, stats, xpReward, goldReward, possibleLoot=items.no_loot, lootChance=-1, imageUrl='', isBoss=False) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward
        self.goldReward = goldReward
        self.possibleLoot = possibleLoot
        self.lootChance = lootChance
        self.imageUrl = imageUrl
        self.isBoss = isBoss

def createEnemy(enemy_json):
    enemy = Enemy(enemy_json['name'], enemy_json['stats'], enemy_json['xpReward'], enemy_json['goldReward'], enemy_json['possibleLoot'], enemy_json['lootChance'], enemy_json['imageUrl'], enemy_json['isBoss'])
    return enemy

# AREA 1:

    # Monsters
class Bat(Enemy):
    def __init__(self) -> None:
        stats = {'maxHp': 15,
                 'hp': 15,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 3,
                 'def': 5,
                 'matk': 1,
                 'mdef': 1,
                 'speed': 12,
                 'critCh': 10
                 }
        super().__init__('Bat', stats, xpReward=4, goldReward=randint(2, 5), possibleLoot=items.item_bat_wings, lootChance=60,
                         imageUrl="https://i.postimg.cc/fLsrwz3Z/Colossal-Bat.png")

class Wolf(Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 22,
                    'hp' : 22,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 4,
                    'def' : 6,
                    'matk' : 1,
                    'mdef' : 2,
                    'speed' : 9,
                    'critCh' : 5
        }
        super().__init__('Wolf', stats, xpReward=8, goldReward=randint(3, 6), possibleLoot=items.item_wolf_fur, lootChance=40, imageUrl="https://i.postimg.cc/1R65TbDJ/Mountain-Wolf.png")

class LionAnt(Enemy):
    def __init__(self):
        stats = {'maxHp': 19,
                 'hp': 19,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 4,
                 'def': 5,
                 'matk': 1,
                 'mdef': 1,
                 'speed': 7,
                 'critCh': 15
                 }
        super().__init__('Lion Ant', stats, xpReward=5, goldReward=randint(4, 20), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/tCq5Dgyc/Insects-Ant-Lion.png")

class ColossalCaterpillar(Enemy):
    def __init__(self):
        stats = {'maxHp': 38,
                 'hp': 38,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 4,
                 'def': 10,
                 'matk': 1,
                 'mdef': 5,
                 'speed': 2,
                 'critCh': 1
                 }
        super().__init__('Colossal Caterpillar', stats, xpReward=25, goldReward=randint(4, 20), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/7PV1Cy7n/Insects-Caterpillar-A.png")

class GiantDragonfly(Enemy):
    def __init__(self):
        stats = {'maxHp': 20,
                 'hp': 20,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 7,
                 'def': 3,
                 'matk': 1,
                 'mdef': 1,
                 'speed': 13,
                 'critCh': 10
                 }
        super().__init__('Giant Dragonfly', stats, xpReward=20, goldReward=randint(12, 20), possibleLoot=items.item_dragonfly_wings, lootChance=50,
                         imageUrl="https://i.postimg.cc/HskwXP9D/Insects-Dragonfly-B.png")

    # Area 1 Boss
class Daidarabotchi(Enemy):
    def __init__(self):
        stats = {'maxHp': 102,
                 'hp': 102,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 10,
                 'def': 10,
                 'matk': 1,
                 'mdef': 10,
                 'speed': 12,
                 'critCh': 5
                 }
        super().__init__('Daidarabotchi, Forest Guardian', stats, xpReward=304, goldReward=104,
                         imageUrl="https://i.postimg.cc/DygrbcK4/Boss-Daidarabotchi.png")
        self.isBoss = True

    # Dungeon Area 1 Monsters
class GoblinRaider(Enemy):
    def __init__(self):
        stats = {'maxHp': 30,
                 'hp': 30,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 7,
                 'def': 6,
                 'matk': 1,
                 'mdef': 4,
                 'speed': 13,
                 'critCh': 10
                 }
        super().__init__('Goblin Raider', stats, xpReward=30, goldReward=randint(12, 20), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/pX2mzsxW/Goblin-Raider.png")

class GoblinArcher(Enemy):
    def __init__(self):
        stats = {'maxHp': 25,
                 'hp': 25,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 6,
                 'def': 4,
                 'matk': 1,
                 'mdef': 7,
                 'speed': 10,
                 'critCh': 20
                 }
        super().__init__('Goblin Archer', stats, xpReward=20, goldReward=randint(12, 20), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/tTXK2ngx/Goblin-Archer.png")

class GoblinElite(Enemy):
    def __init__(self):
        stats = {'maxHp': 40,
                 'hp': 40,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 10,
                 'def': 7,
                 'matk': 1,
                 'mdef': 8,
                 'speed': 5,
                 'critCh': 5
                 }
        super().__init__('Goblin Elite', stats, xpReward=100, goldReward=randint(20, 50), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/VvXHwY58/Goblin-Elite.png")
        self.isBoss = True


area_1_enemies = [Wolf, Bat, LionAnt, ColossalCaterpillar, GiantDragonfly]
area_1_boss = Daidarabotchi

dungeon_1_enemies = [GoblinRaider, GoblinArcher]