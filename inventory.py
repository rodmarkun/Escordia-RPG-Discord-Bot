import json
import skills
import emojis

# Emoji used for money/gold/coins
money_emoji = emojis.ESC_GOLD_ICON

class Inventory():
    '''
    Manages player's inventory and items. Can be modified to have a certain capacity.
    It is also used for shops.
    '''

    def __init__(self, player_name) -> None:
        '''
        Creates a new inventory

        :param player_name: Player owner of this inventory
        '''
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
            if self.items[index-1].objectType != 'Weapon':
                inv_str += f'{index} - {self.items[index-1].show_info()}\n'
            else:
                inv_str += f'{index} - {self.items[index - 1].show_info()}\n'
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

    def check_for_item_and_amount(self, object_name, amount):
        '''
        Checks if player has an X amount of a certain item. Used for crafting.

        :param object_name: Name of the object to check
        :param amount: Amount to check
        :return: True if there is an amount >= X of the item
        '''
        for item in self.items:
            if item.name.lower() == object_name.lower():
                if item.amount >= amount:
                    return True
        return False

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
        '''
        Converts an inventory instance to a JSON

        :return: Inventory JSON
        '''
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def createInventory(inv_json):
    '''
    Creates an inventory from an inventory JSON

    :param inv_json: Inventory JSON
    :return: Inventory instance
    '''
    inv = Inventory(inv_json['player_name'])
    for item in inv_json['items']:
        item_obj = createItem(item)
        inv.add_item(item_obj)
        pass
    return inv

class Item:
    '''
    Items with various functions. Can be stored inside an inventory.
    '''

    def __init__(self, name, description, amount, individualValue, objectType) -> None:
        '''
        Creates an Item

        :param name: Item name
        :param description: Item description
        :param amount: Item amount (In 99% of cases you want this to 1)
        :param individualValue: Individual value of the item
        :param objectType: Object type. Relevant to Icons, Masteries, and other stuff
        '''
        self.name = name
        self.description = description
        self.amount = amount
        self.individualValue = individualValue
        self.objectType = objectType
        if self.objectType:
            self.emoji = emojis.obj_to_emoji[self.objectType]

    def show_info(self):
        '''
        Shows info of a certain item.

        :return: Item info string.
        '''
        return f'[x{self.amount}] {self.emoji} **{self.name}** ({self.objectType}) - {self.individualValue}{money_emoji}'

    def show_info_trader(self):
        '''
        Shows info of a certain item. Formatted without the amount, mainly for traders.

        :return: Item info string.
        '''
        return f'{self.emoji} **{self.name}** ({self.objectType}) - {self.individualValue}{money_emoji}'
    
    def toJSON(self):
        '''
        Converts an item instance into a JSON

        :return: Item JSON
        '''
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def create_item(self):
        '''
        Creates a duplicate from an item. Useful when buying items.

        :return: Item copy
        '''
        return Item(self.name, self.description, self.amount, self.individualValue, self.objectType)

def createItem(item_json):
    '''
    Creates an Item instance from an Item JSON

    :param item_json: Item JSON
    :return: Item instance
    '''
    equipable_items = ['Helmet', 'Armor', 'Weapon', 'Accessory', 'Pickaxe', 'Axe']
    if item_json['objectType'] in equipable_items:
        item = Equipment(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'], item_json['objectSubType'], item_json['statChangeList'])
    elif item_json['objectType'] == 'Potion':
        item = Potion(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'], item_json['stat'], item_json['amountToChange'])
    elif item_json['objectType'] == 'Grimoire':
        item = Grimoire(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'], item_json['spell'])
    else:
        item = Item(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'])
    return item

class Equipment(Item):
    '''
    Items player can equip for increased stats.
    '''

    def __init__(self, name, description, amount, individual_value, objectType, objectSubType, statChangeList) -> None:
        '''
        Creates a new equipment instance.

        :param name: Equipment's name
        :param description: Equipment's description
        :param amount: Amount of this equipment
        :param individual_value: Individual value of this equipment
        :param objectType: Object type of this equipment
        :param objectSubType: Object subtype of this equipment (Mainly used for different types of weapons)
        :param statChangeList: Dictionary that defines the changes in stats after equipping this item.
        Example:
        {'hp' : 3,
        'atk' : 2,
        'speed' : -2
        }
        This would increase hp by 3, atk by 2 and decrease speed by 2.
        '''
        super().__init__(name, description, amount, individual_value, objectType)
        self.objectSubType = objectSubType
        self.statChangeList = statChangeList
        if self.objectType == 'Weapon':
            self.emoji = emojis.weapon_to_emoji[self.objectSubType]

    def show_info_trader(self):
        '''
        Shows info of certain equipment. Formatted without the amount, mainly for traders.

        :return: Item info string.
        '''
        return f'{self.emoji} **{self.name}** ({self.objectType}) [{self.show_stats()}] - {self.individualValue}{money_emoji}'

    def show_info(self):
        '''
        Shows info of certain equipment.

        :return: Item info string.
        '''
        return f'[x{self.amount}] {self.emoji} **{self.name}** ({self.objectType}) [{self.show_stats()}] - {self.individualValue}{money_emoji}'

    def show_stats(self):
        '''
        Shows equipment's stats

        :return: Stat info string
        '''
        statsString = ' '
        for stat in self.statChangeList:
            sign = '+'
            if self.statChangeList[stat] < 0:
                sign = ''
            statsString += f'{stat} {sign}{self.statChangeList[stat]} '
        return statsString

    def create_item(self, amount):
        '''
        Creates a copy of a certain equipment

        :param amount: Amount of copies to be made
        :return: Equipment object
        '''
        return Equipment(self.name, self.description, amount, self.individualValue, self.objectType, self.objectSubType,
                         self.statChangeList)


class Potion(Item):
    '''
    Players use potions for recovering either MP or HP.
    '''

    def __init__(self, name, description, amount, individual_value, objectType, stat, amountToChange) -> None:
        '''
        Creates a new Potion object.

        :param name: Potion name
        :param description: Potion description
        :param amount: Potion amount
        :param individual_value: Individual value
        :param objectType: Object type (Potion)
        :param stat: Stat to change
        :param amountToChange: Amount to change
        '''
        super().__init__(name, description, amount, individual_value, objectType)
        self.stat = stat
        self.amountToChange = amountToChange

    def activate(self, caster):
        '''
        Activates the use of this object. (Recovers HP/MP)

        :param caster: Player which uses the object
        :return: Activation info string
        '''
        if self.stat == 'hp':
            caster.heal(self.amountToChange)
        elif self.stat == 'mp':
            caster.recover_mp(self.amountToChange)
        return f'{caster.name} uses a {self.name} and recovers {self.amountToChange}{self.stat}!'

    def create_item(self, amount):
        '''
        Creates a copy of a certain potion

        :param amount: Amount of copies to be made
        :return: Potion object
        '''
        return Potion(self.name, self.description, amount, self.individualValue, self.objectType, self.stat,
                      self.amountToChange)


class Grimoire(Item):
    '''
    Grimoires are items the player can use for learning new spells.
    '''

    def __init__(self, name, description, amount, individual_value, objectType, spell) -> None:
        '''
        Creates a new Grimoire object

        :param name: Grimoire name
        :param description: Grimoire description
        :param amount: Item amount
        :param individual_value: Individual value
        :param objectType: Object type (Grimoire)
        :param spell: Spell to be learnt
        '''
        super().__init__(name, description, amount, individual_value, objectType)
        self.spell = spell

    def activate(self, caster):
        '''
        Activates the use of this object. (Learns a new spell)

        :param caster: Player which will learn the spell
        :return: Activation info string
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
        '''
        Creates a copy of a certain grimoire

        :param amount: Amount of copies to be made
        :return: Grimoire object
        '''
        return Grimoire(self.name, self.description, amount, self.individualValue, self.objectType, self.spell)