import json

import file_management
import inventory
import combat
import skills
import emojis
from StringProgressBar import progressBar


masteries_leveling = {"lvl" : 1, "xp" : 0, "xpToNextLvl" : 150}
masteries = {"Swords" : masteries_leveling, "Axes & Hammers" : masteries_leveling, "Daggers" : masteries_leveling, "Bows" : masteries_leveling, "Staffs & Scythes" : masteries_leveling}
gathering_equipment = ['Pickaxe', 'Axe']

class Player(combat.Battler):
    '''
    Player class which will hold all the info across the game.
    '''

    def __init__(self, name) -> None:
        '''
        Creates a new player.

        :param name: Player's name.
        '''
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
        self.gathering_equipment = {'Pickaxe' : None,
                                    'Axe' : None}
        self.gathering_tiers = {'miningTier' : 0,
                                 'choppingTier' : 0}
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
        equipment_names ={"Helmet" : "None", "Armor" : "None", "Weapon" : "None", "Accessory" : "None", "Pickaxe" : "None", "Axe" : "None"}
        for item in self.equipment:
            if self.equipment[item] is not None:
                equipment_names[item] = self.equipment[item]['name'] + " " + self.equipment[item]["emoji"]
        for item in self.gathering_equipment:
            if self.gathering_equipment[item] is not None:
                equipment_names[item] = self.gathering_equipment[item]['name'] + " " + self.gathering_equipment[item]["emoji"]

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
               f'**Accessory**: {equipment_names["Accessory"]}\n' \
               f'**----------------**\n' \
               f'**Gathering Pickaxe**: {equipment_names["Pickaxe"]}\n' \
               f'**Gathering Axe**: {equipment_names["Axe"]}\n' \
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

    def show_spells(self):
        '''
        Returns a string with all spells known by the player

        :return: Spells string
        '''
        spell_str = ""
        i = 1
        for spell in self.spells:
            spell_str += f"{i} - **{spell['name']}** [Power: {spell['power']}, MP Cost: {spell['cost']}], \"{spell['description']}\"\n"
            i += 1
        return spell_str

    def show_combos(self):
        '''
        Returns a string with all combos known by the player

        :return: Combos string
        '''
        combo_str = ""
        i = 1
        for combo in self.combos:
            combo_str += f"{i} - **{combo['name']}** [Combo Points: {combo['cost']}], \"{combo['description']}\"\n"
            i += 1
        return combo_str

    def show_masteries(self):
        '''
        Shows player's materies

        :return: Masteries string
        '''
        masteries_dict = file_management.get_masteries(self)
        info_txt = ""
        for mastery in masteries_dict["masteries"]:
            mastery_bar = progressBar.filledBar(masteries_dict["masteries"][mastery]["xpToNextLvl"], masteries_dict["masteries"][mastery]["xp"], size=10)
            info_txt += f'{emojis.weapon_to_emoji[mastery]} **{mastery}** - LVL: {masteries_dict["masteries"][mastery]["lvl"]} - {mastery_bar[0]} \n'
        return info_txt

    def normal_attack(self, defender):
        '''
        Performs a normal attack, same as Battler's but adding a Combo Point.

        :param defender:
        :return: Attack info string
        '''
        #self.addComboPoints(1)
        return super().normal_attack(defender)


    def equip_item(self, equipment):
        '''
        Player equips certain item. Must be of type 'Equipment'.
    
        :param equipment: Equipment to be equipped
        '''
        info = ''
        if type(equipment) == inventory.Equipment:
            if equipment.objectType not in gathering_equipment:
                if self.equipment[equipment.objectType] is not None:
                    actualEquipment = inventory.createItem(self.equipment[equipment.objectType])
                    info += f'{actualEquipment.name} has been unequiped.\n'
                    self.inventory.add_item(actualEquipment)
                    for stat in actualEquipment.statChangeList:
                        self.stats[stat] -= actualEquipment.statChangeList[stat]
            else:
                if self.gathering_equipment[equipment.objectType] is not None:
                    actualEquipment = inventory.createItem(self.gathering_equipment[equipment.objectType])
                    info += f'{actualEquipment.name} has been unequiped.\n'
                    self.inventory.add_item(actualEquipment)

            # Adds stats to player
            if equipment.objectType not in gathering_equipment:
                for stat in equipment.statChangeList:
                    self.stats[stat] += equipment.statChangeList[stat]
                self.equipment[equipment.objectType] = equipment.create_item(1)
            else:
                for gath_tier in equipment.statChangeList:
                    self.gathering_tiers[gath_tier] = equipment.statChangeList[gath_tier]
                self.gathering_equipment[equipment.objectType] = equipment.create_item(1)

            self.inventory.decrease_item_amount(equipment, 1)
            info += f'{equipment.name} has been equipped.'
        else:
            if equipment is not None:
                print(type(equipment))
                info += f'{equipment.name} is not equipable.'
        return info

    def use_item(self, item):
        '''
        Uses a certain item. Item must be in the "usable_items" list
        to be used.

        :param item: Item to be used
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

        :param exp: Exp points to be added to player's exp
        '''
        lvl_up_str = ""
        self.xp += exp
        if self.equipment["Weapon"] is not None:
            lvl_up_str += file_management.update_masteries(self, self.equipment["Weapon"]["objectSubType"], exp)
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
            lvl_up_str += f"Level up! You are now level {self.lvl}. Your HP and MP have been restored. You now have {self.aptitudePoints} aptitude points"
        return lvl_up_str

    def add_money(self, money):
        '''
        Adds a certain amount of money to the player.

        :param money: Money to be added
        '''
        self.money += money

    def update_stats_to_aptitudes(self, aptitude, points):
        '''
        Assigns the corresponding stat points when upgrading aptitudes.

        :param aptitude: Aptitude to be updated
        :param points: Points spent to level up aptitude
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

        :param points: Combo points to be added
        '''
        self.comboPoints += points

    def death(self):
        '''
        Performs all actions needed when a player dies
        '''
        self.inDungeon = False
        file_management.delete_dungeon(self.name)
        self.money = round(self.money / 2)
        combat.fully_heal(self)
        combat.fully_recover_mp(self)

    def toJSON(self):
        '''
        Converts a player instance to a JSON string

        :return: Player JSON
        '''
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
                        "gathering_equipment" : self.gathering_equipment,
                        "money" : self.money,
                        "isAlly" : self.isAlly,
                        "currentArea" : self.currentArea,
                        "defeatedBosses" : self.defeatedBosses,
                        "inDungeon" : self.inDungeon,
                        "gathering_tiers" : self.gathering_tiers,
                        "combos" : self.combos,
                        "spells" : self.spells}
        return json.dumps(player_data, default=lambda o: o.__dict__, sort_keys=True)

def createPlayer(player_json):
    '''
    Converts a player JSON into a player instance

    :param player_json: Player KSON
    :return: Player instance
    '''
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
    player.gathering_equipment = player_json['gathering_equipment']
    player.money = player_json['money']
    player.isAlly = player_json['isAlly']
    player.currentArea = player_json['currentArea']
    player.defeatedBosses = player_json['defeatedBosses']
    player.inDungeon = player_json['inDungeon']
    player.gathering_tiers = player_json['gathering_tiers']
    player.spells = player_json['spells']
    player.combos = player_json['combos']
    player.inventory = file_management.get_inventory(player.name)
    return player

# Deprecated
class PlayerEncoder(json.JSONEncoder):
    def default(self, obj):
        return [obj.name, obj.stats, obj.lvl, obj.xp, obj.xpToNextLvl, obj.comboPoints, obj.aptitudes, obj.aptitudePoints, obj.equipment, obj.money, obj.combos, obj.spells, obj.activeQuests, obj.completedQuests, obj.isAlly]