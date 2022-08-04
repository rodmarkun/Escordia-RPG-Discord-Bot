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

class Wolf(Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 18,
                    'hp' : 18,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 3,
                    'def' : 6,
                    'matk' : 1,
                    'mdef' : 2,
                    'speed' : 9,
                    'critCh' : 5
        }
        super().__init__('Wolf', stats, xpReward=8, goldReward=randint(3, 6), imageUrl="https://i.postimg.cc/1R65TbDJ/Mountain-Wolf.png")

# # Possible Enemy : (LowestPlayerLevelForAppearing, HighestPlayerLevelForAppearing)
# possible_enemies = {Slime: (1, 2),
#                     Imp : (1, 4),
#                     Golem : (3, 10),
#                     GiantSlime : (4, 100),
#                     Bandit : (4, 100)}
#
# # Fixed Combat Enemies
# enemy_list_caesarus_bandit = [CaesarusBandit(), Bandit(), Bandit()]