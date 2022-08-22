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
    possibleLoot : Item
        Item(s) the enemy can drop when defeated
    lootChance : int
        Chance to get the loot
    imageUrl : String
        URL of enemy's image
    isBoss : Bool
        Whether the enemy is a boss or not
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

    # Enemies
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
        stats = {'maxHp' : 25,
                    'hp' : 25,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 5,
                    'def' : 6,
                    'matk' : 1,
                    'mdef' : 3,
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
                 'atk': 5,
                 'def': 7,
                 'matk': 1,
                 'mdef': 3,
                 'speed': 7,
                 'critCh': 15
                 }
        super().__init__('Lion Ant', stats, xpReward=5, goldReward=randint(3, 6), possibleLoot=items.no_loot, lootChance=-1,
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
                 'mdef': 8,
                 'speed': 2,
                 'critCh': 1
                 }
        super().__init__('Colossal Caterpillar', stats, xpReward=25, goldReward=randint(4, 9), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/7PV1Cy7n/Insects-Caterpillar-A.png")

class GiantDragonfly(Enemy):
    def __init__(self):
        stats = {'maxHp': 22,
                 'hp': 22,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 7,
                 'def': 3,
                 'matk': 1,
                 'mdef': 3,
                 'speed': 13,
                 'critCh': 10
                 }
        super().__init__('Giant Dragonfly', stats, xpReward=20, goldReward=randint(5, 10), possibleLoot=items.item_dragonfly_wings, lootChance=50,
                         imageUrl="https://i.postimg.cc/HskwXP9D/Insects-Dragonfly-B.png")

    # Area 1 Boss
class Daidarabotchi(Enemy):
    def __init__(self):
        stats = {'maxHp': 102,
                 'hp': 102,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 10,
                 'def': 8,
                 'matk': 1,
                 'mdef': 10,
                 'speed': 12,
                 'critCh': 5
                 }
        super().__init__('Daidarabotchi, Forest Guardian', stats, xpReward=304, goldReward=104,
                         imageUrl="https://i.postimg.cc/DygrbcK4/Boss-Daidarabotchi.png")
        self.isBoss = True

    # Dungeon 01 Area 1 Monsters
class GoblinRaider(Enemy):
    def __init__(self):
        stats = {'maxHp': 35,
                 'hp': 35,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 7,
                 'def': 7,
                 'matk': 1,
                 'mdef': 5,
                 'speed': 13,
                 'critCh': 10
                 }
        super().__init__('Goblin Raider', stats, xpReward=30, goldReward=randint(8, 16), possibleLoot=items.no_loot, lootChance=-1,
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
        super().__init__('Goblin Archer', stats, xpReward=20, goldReward=randint(8, 16), possibleLoot=items.no_loot, lootChance=-1,
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
                 'mdef': 9,
                 'speed': 5,
                 'critCh': 5
                 }
        super().__init__('Goblin Elite', stats, xpReward=100, goldReward=randint(20, 50), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/VvXHwY58/Goblin-Elite.png")
        self.isBoss = True

# AREA 2:

    # Area 2 Enemies:
class RogueSwordsman(Enemy):
    def __init__(self):
        stats = {'maxHp': 50,
                 'hp': 50,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 12,
                 'def': 8,
                 'matk': 1,
                 'mdef': 7,
                 'speed': 7,
                 'critCh': 10
                 }
        super().__init__('Rogue Swordsman', stats, xpReward=50, goldReward=randint(20, 50), possibleLoot=items.item_rogue_badge, lootChance=50,
                         imageUrl="https://i.postimg.cc/Kck0mvrf/Rogue-Bastard-Sword.png")

class RogueMonk(Enemy):
    def __init__(self):
        stats = {'maxHp': 50,
                 'hp': 50,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 10,
                 'def': 13,
                 'matk': 1,
                 'mdef': 11,
                 'speed': 13,
                 'critCh': 15
                 }
        super().__init__('Rogue Monk', stats, xpReward=45, goldReward=randint(0, 30), possibleLoot=items.item_rogue_badge, lootChance=50,
                         imageUrl="https://i.postimg.cc/MpDD9cq6/Rogue-Dagger-Monk.png")

class RogueAssasin(Enemy):
    def __init__(self):
        stats = {'maxHp': 45,
                 'hp': 45,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 12,
                 'def': 7,
                 'matk': 1,
                 'mdef': 7,
                 'speed': 22,
                 'critCh': 25
                 }
        super().__init__('Rogue Assasin', stats, xpReward=42, goldReward=randint(20, 45), possibleLoot=items.item_rogue_badge, lootChance=50,
                         imageUrl="https://i.postimg.cc/q7DGd9NW/Rogue-Twin-Dagger.png")

class EarthWorm(Enemy):
    def __init__(self):
        stats = {'maxHp': 70,
                 'hp': 70,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 9,
                 'def': 12,
                 'matk': 1,
                 'mdef': 12,
                 'speed': 5,
                 'critCh': 5
                 }
        super().__init__('Earth Worm', stats, xpReward=55, goldReward=randint(15, 32), possibleLoot=items.item_earthworm_tooth, lootChance=20,
                         imageUrl="https://i.postimg.cc/MpW0fWRh/Cave-Dweller-Worm.png")

class MountainHarpy(Enemy):
    def __init__(self):
        stats = {'maxHp': 40,
                 'hp': 40,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 12,
                 'def': 5,
                 'matk': 1,
                 'mdef': 10,
                 'speed': 25,
                 'critCh': 10
                 }
        super().__init__('Mountain Harpy', stats, xpReward=30, goldReward=randint(15, 32), possibleLoot=items.item_harpy_feather, lootChance=40,
                         imageUrl="https://i.postimg.cc/jdPjyPK1/Wind-Harpy.png")

    # Area 2 Boss:
class RogueMasterGarland(Enemy):
    def __init__(self):
        stats = {'maxHp': 235,
                 'hp': 235,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 20,
                 'def': 15,
                 'matk': 1,
                 'mdef': 16,
                 'speed': 20,
                 'critCh': 10
                 }
        super().__init__('Rogue Master Garland', stats, xpReward=705, goldReward=357,
                         imageUrl="https://i.postimg.cc/6Tx8VQFC/Assasin-Garland.png")
        self.isBoss = True

    # Dungeon 02 Area 2 Monsters
class SkeletonGuard(Enemy):
    def __init__(self):
        stats = {'maxHp': 60,
                 'hp': 60,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 11,
                 'def': 9,
                 'matk': 1,
                 'mdef': 10,
                 'speed': 15,
                 'critCh': 10
                 }
        super().__init__('Skeleton Guard', stats, xpReward=90, goldReward=randint(20, 50), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/Y9bggypB/Skeleton-Knight-Debon.png")

class SkeletonHero(Enemy):
    def __init__(self):
        stats = {'maxHp': 60,
                 'hp': 60,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 14,
                 'def': 6,
                 'matk': 1,
                 'mdef': 8,
                 'speed': 20,
                 'critCh': 10
                 }
        super().__init__('Skeleton Hero', stats, xpReward=100, goldReward=randint(18, 38), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/8PFWJH9x/Skeleton-Knight-Alstreim.png")

class SkeletonKnight(Enemy):
    def __init__(self):
        stats = {'maxHp': 70,
                 'hp': 70,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 9,
                 'def': 12,
                 'matk': 1,
                 'mdef': 12,
                 'speed': 5,
                 'critCh': 10
                 }
        super().__init__('Skeleton Knight', stats, xpReward=100, goldReward=randint(15, 55), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/qB6ygw9S/Skeleton-Knight-Baron.png")

class SkeletonDragon(Enemy):
    def __init__(self):
        stats = {'maxHp': 120,
                 'hp': 120,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 12,
                 'def': 14,
                 'matk': 1,
                 'mdef': 15,
                 'speed': 10,
                 'critCh': 15
                 }
        super().__init__('Skeleton Dragon', stats, xpReward=300, goldReward=randint(100, 180), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/G2q72QVH/Skeleton-Dragon.png")
        self.isBoss = True

    # Dungeon 03 Area 2
class BlackAntKnight(Enemy):
    def __init__(self):
        stats = {'maxHp': 65,
                 'hp': 65,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 13,
                 'def': 12,
                 'matk': 1,
                 'mdef': 10,
                 'speed': 15,
                 'critCh': 10
                 }
        super().__init__('Black Ant Knight', stats, xpReward=100, goldReward=randint(15, 55), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/SRhmq1m9/Insects-Black-Ant-Knight.png")

class BlackAntBerserker(Enemy):
    def __init__(self):
        stats = {'maxHp': 74,
                 'hp': 74,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 14,
                 'def': 12,
                 'matk': 1,
                 'mdef': 10,
                 'speed': 5,
                 'critCh': 1
                 }
        super().__init__('Black Ant Berserker', stats, xpReward=100, goldReward=randint(15, 55), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/vZcwRw5j/Insects-Black-Ant-Berserker.png")

class BlackAntArcher(Enemy):
    def __init__(self):
        stats = {'maxHp': 62,
                 'hp': 62,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 8,
                 'def': 8,
                 'matk': 1,
                 'mdef': 8,
                 'speed': 5,
                 'critCh': 30
                 }
        super().__init__('Black Ant Archer', stats, xpReward=100, goldReward=randint(15, 55), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/mkbK8vbm/Insects-Black-Ant-Archer.png")

class BlackAntProtector(Enemy):
    def __init__(self):
        stats = {'maxHp': 80,
                 'hp': 80,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 7,
                 'def': 18,
                 'matk': 1,
                 'mdef': 13,
                 'speed': 5,
                 'critCh': 1
                 }
        super().__init__('Black Ant Knight', stats, xpReward=100, goldReward=randint(15, 55), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/RhXy8gh4/Insects-Black-Ant-Protector.png")

class BlackAntQueen(Enemy):
    def __init__(self):
        stats = {'maxHp': 180,
                 'hp': 180,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 18,
                 'def': 12,
                 'matk': 1,
                 'mdef': 12,
                 'speed': 20,
                 'critCh': 10
                 }
        super().__init__('Black Ant Queen', stats, xpReward=300, goldReward=randint(100, 180), possibleLoot=items.no_loot, lootChance=-1,
                         imageUrl="https://i.postimg.cc/sfckvgcq/Boss-Black-Ant-Queen.png")
        self.isBoss = True

area_1_enemies = [Wolf, Bat, LionAnt, ColossalCaterpillar, GiantDragonfly]
area_1_boss = Daidarabotchi

area_2_enemies = [RogueSwordsman, RogueMonk, RogueAssasin, EarthWorm, MountainHarpy]
area_2_boss = RogueMasterGarland

dungeon_1_enemies = [GoblinRaider, GoblinArcher]
dungeon_2_enemies = [SkeletonHero, SkeletonGuard, SkeletonKnight]
dungeon_3_enemies = [BlackAntKnight, BlackAntBerserker, BlackAntArcher, BlackAntProtector]