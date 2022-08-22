import json

import inventory
#import text
import combat
import skills


class Player(combat.Battler):
    '''
    Player class which will hold all the info across the game. Will be stored in "players.txt" and the inventory
    will be stored in "inventory.txt"
    '''

    def __init__(self, name) -> None:
        stats = {'maxHp': 25,
                 'hp': 25,
                 'maxMp': 10,
                 'mp': 10,
                 'atk': 10,
                 'def': 10,
                 'matk': 10,
                 'mdef': 10,
                 'speed': 10,
                 'critCh': 10
                 }

        super().__init__(name, stats)

        self.lvl = 1  # Player Lvl
        self.xp = 0  # Current xp
        self.xpToNextLvl = 15  # Amount of xp to reach next lvl is multiplied by 1.5 per level
        self.comboPoints = 0
        self.aptitudes = {'str': 5,
                          'dex': 5,
                          'int': 5,
                          'wis': 5,
                          'const': 5
                          }

        self.aptitudePoints = 0  # Points for upgrading aptitudes
        self.inventory = inventory.Inventory(self.name)  # Player's inventory
        self.equipment = {  'Helmet' : None,
                            'Armor': None,
                            'Weapon': None,
                            'Accessory' : None}  # Player's equipment, can be further expanded
        self.money = 20  # Current money
        self.combos = []  # Player's selection of combos (atk, cp)
        self.spells = []  # Player's selection of spells (matk, mp)

        self.currentArea = 1
        self.defeatedBosses = 0
        self.inDungeon = False

        self.isAlly = True  # Check if battler is an ally or not

    def show_info(self):
        '''
        Shows all the current info (profile) about the player.

        :return: Info string
        '''
        equipment_names ={"Helmet" : "None", "Armor" : "None", "Weapon" : "None", "Accessory" : "None"}
        for item in self.equipment:
            if self.equipment[item] is not None:
                equipment_names[item] = self.equipment[item]['name']

        return f'**Player Name**: {self.name}\n' \
               f'**Level**: {self.lvl}\n' \
               f'**Xp**: {self.xp}\n' \
               f'**Xp to next level**: {self.xpToNextLvl-self.xp}\n' \
               f'**---STATS---**\n' \
               f'**MAXHP**: {self.stats["maxHp"]}\n' \
               f'**HP**: {self.stats["hp"]}\n' \
               f'**MAXMP**: {self.stats["maxMp"]}\n' \
               f'**MP**: {self.stats["mp"]}\n' \
               f'**ATK**: {self.stats["atk"]}\n' \
               f'**DEF**: {self.stats["def"]}\n' \
               f'**MATK**: {self.stats["matk"]}\n' \
               f'**MDEF**: {self.stats["mdef"]}\n' \
               f'**SPEED**: {self.stats["speed"]}\n' \
               f'**CRITCH**: {self.stats["critCh"]}\n' \
               f'**---APTITUDES---**\n' \
               f'**STR**: {self.aptitudes["str"]}\n' \
               f'**DEX**: {self.aptitudes["dex"]}\n' \
               f'**INT**: {self.aptitudes["int"]}\n' \
               f'**WIS**: {self.aptitudes["wis"]}\n' \
               f'**CONST**: {self.aptitudes["const"]}\n' \
               f'**---EQUIPMENT---**\n' \
               f'**Helmet**: {equipment_names["Helmet"]}\n' \
               f'**Armor**: {equipment_names["Armor"]}\n' \
               f'**Weapon**: {equipment_names["Weapon"]}\n' \
               f'**Accesory**: {equipment_names["Accessory"]}\n' \
               f'**----------------**\n' \
               f'**Aptitude Points**: {self.aptitudePoints}\n' \
               f'**Money**: {self.money}\n' \
               f'**Bosses Defeated**: {self.defeatedBosses}\n'


    def show_aptitudes(self):
        '''
        Shows current player's aptitudes

        :return: Info string
        '''
        return f'**STR**: {self.aptitudes["str"]} - [+2 ATK]\n' \
               f'**DEX**: {self.aptitudes["dex"]} - [+1 ATK, +1 SPEED, +1 CRITCH]\n' \
               f'**INT**: {self.aptitudes["int"]} - [+2 MATK]\n' \
               f'**WIS**: {self.aptitudes["wis"]} - [+3 MAXMP, +2 MDEF]\n' \
               f'**CONST**: {self.aptitudes["const"]} - [+2 MAXHP, +2 DEF]\n\n' \
               f'To upgrade an aptitude, use `!aptitudes [aptitude_name] [points]`\n' \
               f'Example: `!aptitudes dex 1`\n' \
               f'You currently have {self.aptitudePoints} aptitude points.'

    def normal_attack(self, defender):
        '''
        Performs a normal attack, same as Battler's but adding a Combo Point.
        :param defender:
        :return:
        '''
        self.addComboPoints(1)
        return super().normal_attack(defender)


    def equip_item(self, equipment):
        '''
        Player equips certain item. Must be of type 'Equipment'.
    
        Parameters:
        equipment : Equipment
            Item to equip.
        '''
        info = ''
        if type(equipment) == inventory.Equipment:
            if self.equipment[equipment.objectType] is not None:
                actualEquipment = inventory.createItem(self.equipment[equipment.objectType])
                info += f'{actualEquipment.name} has been unequiped.\n'
                self.inventory.add_item(actualEquipment)
                for stat in actualEquipment.statChangeList:
                    self.stats[stat] -= actualEquipment.statChangeList[stat]

            # Adds stats to player
            for stat in equipment.statChangeList:
                self.stats[stat] += equipment.statChangeList[stat]
            self.equipment[equipment.objectType] = equipment.create_item(1)

            self.inventory.decrease_item_amount(equipment, 1)
            info += f'{equipment.name} has been equipped.'
            print(equipment.show_stats())
        else:
            if equipment is not None:
                info += f'{equipment.name} is not equipable.'
        return info

    def use_item(self, item):
        '''
        Uses a certain item. Item must be in the "usable_items" list
        to be used.

        Parameters:
        item : Item
            Item to be used.
        '''
        usable_items = [inventory.Potion, inventory.Grimoire]
        info = 'That item is not usable.'
        if type(item) in usable_items:
            info = item.activate(self)
        self.inventory.decrease_item_amount(item, 1)
        return info

    def add_exp(self, exp):
        '''
        Adds a certain amount of exp to the player and also handles leveling up.
        When leveling up, player also recovers hp/mp fully and has a +1 to all stats.

        Parameters:
        exp : int
            Amount of exp points to add.
        '''
        lvl_up_str = ""
        self.xp += exp
        #print(f"You earn {exp}xp")
        # Level up:
        while self.xp >= self.xpToNextLvl:
            self.xp -= self.xpToNextLvl
            self.lvl += 1
            # You can change this formula for different exp progression
            self.xpToNextLvl = round(self.xpToNextLvl * 1.25 + 10 * self.lvl * self.lvl/2)
            for stat in self.stats:
                self.stats[stat] += 1
            self.aptitudePoints += 1
            combat.fully_heal(self)
            combat.fully_recover_mp(self)
            lvl_up_str = f"Level up! You are now level {self.lvl}. Your HP and MP have been restored. You now have {self.aptitudePoints} aptitude points"
        return lvl_up_str

    def add_money(self, money):
        '''
        Adds a certain amount of money to the player.

        Parameters:
        money : int
            Amount of money to be added.
        '''
        self.money += money

    def update_stats_to_aptitudes(self, aptitude, points):
        '''
        Assigns the corresponding stat points when upgrading aptitudes.

        Parameters:
        aptitude : str
            Aptitude to be upgraded.
        points : int
            Points used to upgrade
        '''
        if aptitude == 'str':
            self.stats['atk'] += 2 * points
        elif aptitude == 'dex':
            self.stats['atk'] += points
            self.stats['speed'] += points
            self.stats['critCh'] += points
        elif aptitude == 'int':
            self.stats['matk'] += 2 * points
        elif aptitude == 'wis':
            self.stats['maxMp'] += 3 * points
            self.stats['mdef'] += 2 * points
        elif aptitude == 'const':
            self.stats['maxHp'] += 2 * points
            self.stats['def'] += 2 * points

    def addComboPoints(self, points):
        '''
        Adds a certain amount of combo points.

        Parameters:
        points : int
            Amount of points to be added.
        '''
        self.comboPoints += points

    def toJSON(self):
        player_data = { "name" : self.name,
                        "stats" : self.stats,
                        "lvl" : self.lvl,
                        "xp" : self.xp,
                        "alive" : self.alive,
                        "xpToNextLvl" : self.xpToNextLvl,
                        "comboPoints" : self.comboPoints,
                        "aptitudes" : self.aptitudes,
                        "aptitudePoints" : self.aptitudePoints,
                        "equipment" : self.equipment,
                        "money" : self.money,
                        "isAlly" : self.isAlly,
                        "currentArea" : self.currentArea,
                        "defeatedBosses" : self.defeatedBosses,
                        "inDungeon" : self.inDungeon,
                        "combos" : self.combos,
                        "spells" : self.spells}
        return json.dumps(player_data, default=lambda o: o.__dict__, sort_keys=True)

def createPlayer(player_json):
    player = Player(player_json['name'])
    player.stats = player_json['stats']
    player.lvl = player_json['lvl']
    player.xp = player_json['xp']
    player.alive = player_json['alive']
    player.xpToNextLvl = player_json['xpToNextLvl']
    player.comboPoints = player_json['comboPoints']
    player.aptitudes = player_json['aptitudes']
    player.aptitudePoints = player_json['aptitudePoints']
    player.equipment = player_json['equipment']
    player.money = player_json['money']
    player.isAlly = player_json['isAlly']
    player.currentArea = player_json['currentArea']
    player.defeatedBosses = player_json['defeatedBosses']
    player.inDungeon = player_json['inDungeon']
    player.spells = player_json['spells']
    player.combos = player_json['combos']
    return player

class PlayerEncoder(json.JSONEncoder):
    def default(self, obj):
        return [obj.name, obj.stats, obj.lvl, obj.xp, obj.xpToNextLvl, obj.comboPoints, obj.aptitudes, obj.aptitudePoints, obj.equipment, obj.money, obj.combos, obj.spells, obj.activeQuests, obj.completedQuests, obj.isAlly]