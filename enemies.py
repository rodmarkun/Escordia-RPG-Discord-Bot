from random import randint
import combat

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
    def __init__(self, name, stats, xpReward, goldReward, imageUrl) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward
        self.goldReward = goldReward
        self.imageUrl = imageUrl

def createEnemy(enemy_json):
    enemy = Enemy(enemy_json['name'], enemy_json['stats'], enemy_json['xpReward'], enemy_json['goldReward'], enemy_json['imageUrl'])
    return enemy

class Bat(Enemy):
    def __init__(self) -> None:
        stats = {'maxHp': 11,
                 'hp': 11,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 3,
                 'def': 5,
                 'matk': 1,
                 'mdef': 1,
                 'speed': 12,
                 'critCh': 5
                 }
        super().__init__('Bat', stats, xpReward=5, goldReward=randint(2, 5),
                         imageUrl="https://i.postimg.cc/fLsrwz3Z/Colossal-Bat.png")

class Wolf(Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 18,
                    'hp' : 18,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 4,
                    'def' : 6,
                    'matk' : 1,
                    'mdef' : 2,
                    'speed' : 9,
                    'critCh' : 5
        }
        super().__init__('Wolf', stats, xpReward=8, goldReward=randint(3, 6), imageUrl="https://i.postimg.cc/1R65TbDJ/Mountain-Wolf.png")



enemies_by_zones = {1 : [Wolf, Bat]}