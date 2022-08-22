import json
import skills
import emojis

class Inventory():
    '''
    Manages player's inventory and items. Can be modified to have a certain capacity.
    It is also used for shops.

    Attributes:
    player_name : String
        Owner's name of the inventory
    items : List
        List of current items in the inventory
    '''

    def __init__(self, player_name) -> None:
        self.player_name = player_name
        self.items = []

    def show_inventory(self):
        '''
        Shows all items from inventory, indexed

        :return: inv_str: String which contains all items from inventory
        '''
        index = 1
        inv_str = ""

        for i in self.items:
            inv_str += f'{index} - {emojis.obj_to_emoji[self.items[index-1].objectType]} {self.items[index-1].show_info()}\n'
            index += 1
        return inv_str

    def get_amount_item(self, index):
        '''
        Gets the amount of X item in the inventory

        :param index: Index of item
        :return: Amount of that item
        '''
        item = self.items[index]
        return item.amount

    def drop_item(self, item_index, amount):
        '''
        Drops an item from the inventory

        :param item_index: Index of item
        :param amount: Amount to drop
        :return: Info string
        '''
        if item_index <= len(self.items):
            item = self.items[item_index - 1]
            if item.drop(amount):
                if item.amount <= 0:
                    self.items.pop(item_index - 1)
                return f'You have succesfully dropped {amount} {item.name}(s)'
            else:
                return f'You do not have that many {item.name}'
        else:
            return f'There is no object in your inventory with index {item_index}'

    def sell_item(self, item_index, amount):
        '''
        Sells an item from the inventory

        :param item_index: Index of item to sell
        :param amount: Amount to sell
        :return: Money returned
        '''
        money_returned = 0
        if item_index <= len(self.items):
            item = self.items[item_index - 1]
            money_returned = round(item.individualValue * amount * 0.5)
            self.decrease_item_amount(item, amount)
        return money_returned

    def add_item(self, new_item):
        '''
        Adds an item to the inventory or increments its amount if it already was in the inventory

        :param new_item: Item to be added
        '''
        alreadyInInventory = False
        for item in self.items:
            if item.name == new_item.name:
                item.amount += new_item.amount
                alreadyInInventory = True
                break
        if not alreadyInInventory:
            self.items.append(new_item)
        
    def equip_item(self, item_index):
        '''
        Checks if an item from the inventory is equipable

        :param item_index: Index of item to equip
        :return: Item
        '''
        if item_index <= len(self.items):
            item = self.items[item_index- 1]
            if type(item) == Equipment:
                return item
            else:
                print('Please choose an equipable object.')
                return None

    def decrease_item_amount(self, item, amount):
        '''
        Decreases X amount of a certain item

        :param item: Item to decrease
        :param amount: Amount to decrease
        '''
        for actualItem in self.items:
            if item.name == actualItem.name:
                actualItem.amount -= amount
                if actualItem.amount <= 0:
                    self.items.remove(actualItem)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def createInventory(inv_json):
    inv = Inventory(inv_json['player_name'])
    for item in inv_json['items']:
        item_obj = createItem(item)
        inv.add_item(item_obj)
        pass
    return inv

class Item():
    '''
    Items are always stored in a certain inventory. They can be either:
    - Equipment (Weapons & Armor)
    - Consumables (Potions & Grimoires)

    Attributes:
    name : str
        Name of the item
    description : str
        Description of the item
    amount : int
        Amount of this item in this inventory
    individualValue : int
        Amount of gold one of this item is worth
    objectType : str
        Object type
    '''


    def __init__(self, name, description, amount, individualValue, objectType) -> None:
        self.name = name
        self.description = description
        self.amount = amount
        self.individualValue = individualValue
        self.objectType = objectType

    def show_info(self):
        '''
        Shows the info of this specific object.

        Returns:
        info : str
            String with amount, name, objectType and individual value of this object.
        '''
        return f'[x{self.amount}] **{self.name}** ({self.objectType}) - {self.individualValue}G'

    def show_info_trader(self):
        '''
        Shows the info of this specific object.

        Returns:
        info : str
            String with amount, name, objectType and individual value of this object.
        '''
        return f'**{self.name}** ({self.objectType}) - {self.individualValue}G'
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def createItem(item_json):
    equipable_items = ['Helmet', 'Armor', 'Weapon', 'Accessory']
    if item_json['objectType'] in equipable_items:
        item = Equipment(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'], item_json['statChangeList'])
    elif item_json['objectType'] == 'Potion':
        item = Potion(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'], item_json['stat'], item_json['amountToChange'])
    elif item_json['objectType'] == 'Grimoire':
        item = Grimoire(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'], item_json['spell'])
    else:
        item = Item(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'])
    return item

class Equipment(Item):
    '''
    Items player can equip for increased stats and unique abilities (combos).

    Parameters:
    statChangeList : Dictionary
        Dictionary that defines the changes in stats after equipping this item.
        Example:
        {'hp' : 3,
        'atk' : 2,
        'speed' : -2
        }
        This would increase hp by 3, atk by 2 and decrease speed by 2.
    '''

    def __init__(self, name, description, amount, individual_value, objectType, statChangeList) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.statChangeList = statChangeList

    def show_info_trader(self):
        return f'**{self.name}** ({self.objectType}) [{self.show_stats()}] - {self.individualValue}G'

    def show_info(self):
        return f'[x{self.amount}] **{self.name}** ({self.objectType}) [{self.show_stats()}] - {self.individualValue}G'

    def show_stats(self):
        '''
        Shows this equipment stats.

        Returns:
        statsString : str
            String which contains all the stat changes of this equipment.
        '''
        statsString = ' '
        for stat in self.statChangeList:
            sign = '+'
            if self.statChangeList[stat] < 0:
                sign = ''
            statsString += f'{stat} {sign}{self.statChangeList[stat]} '
        return statsString

    def create_item(self, amount):
        return Equipment(self.name, self.description, amount, self.individualValue, self.objectType,
                         self.statChangeList)


class Potion(Item):
    '''
    Players use potions for recovering either MP or HP.

    Attributes:
    stat : str
        Stat to recover
    amountToChange : int
        Amount to recover
    '''

    def __init__(self, name, description, amount, individual_value, objectType, stat, amountToChange) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.stat = stat
        self.amountToChange = amountToChange

    def activate(self, caster):
        '''
        Activates the use of this object. (Recovers HP/MP)

        Parameters:
        caster : Player
            Player to recover.
        '''
        if self.stat == 'hp':
            caster.heal(self.amountToChange)
        elif self.stat == 'mp':
            caster.recover_mp(self.amountToChange)
        return f'{caster.name} uses a {self.name} and recovers {self.amountToChange}{self.stat}!'

    def create_item(self, amount):
        return Potion(self.name, self.description, amount, self.individualValue, self.objectType, self.stat,
                      self.amountToChange)


class Grimoire(Item):
    '''
    Grimoires are items the player can use for learning new spells.

    Attributes:
    spell : Spell
        Spell the player will learn.
    '''

    def __init__(self, name, description, amount, individual_value, objectType, spell) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.spell = spell

    def activate(self, caster):
        '''
        Activates the use of this object. (Learns a new spell)

        Parameters:
        caster : Player
            Player which learns the spell.
        '''
        alreadyLearnt = False
        spell_learnt = skills.createSpell(self.spell)
        for skill in caster.spells:
            if skill['name'] == spell_learnt.name:
                alreadyLearnt = True
                break
        if alreadyLearnt:
            return 'You already know this spell.'
        else:
            caster.spells.append(spell_learnt)
            print(caster.spells)
            return f'Using a \"{self.name}\" you have learnt to cast: \"{spell_learnt.name}\"!'

    def create_item(self, amount):
        return Grimoire(self.name, self.description, amount, self.individualValue, self.objectType, self.spell)