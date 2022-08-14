import json

class Inventory():
    '''
    Manages player's inventory and items. Can be modified to have a certain capacity.
    It is also used for shops.

    Attributes:
    items : List
        List of current items in the inventory
    '''

    def __init__(self) -> None:
        self.items = []

    def show_inventory(self):
        '''
        Shows all items from the inventory (indexed).
        '''
        index = 1
        inv_str = ""
        print(self.items)
        for i in self.items:
            inv_str += f'{index} - {self.items[index-1].show_info()}\n'
            index += 1
        return inv_str

    def get_amount_item(self, index):
        item = self.items[index]
        return item.amount

    def drop_item(self, item_index, amount):
        '''
        Drops a certain item from the inventory.
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
        Sells an item from the inventory.

        Returns:
        money_returned : int
            Amount of money for item(s) sold.
        '''
        money_returned = 0
        if item_index <= len(self.items):
            item = self.items[item_index - 1]
            money_returned = round(item.individualValue * amount * 0.5)
            self.decrease_item_amount(item, amount)
        return money_returned

    def add_item(self, new_item):
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
        Selects and equips a certain item from inventory (must be type 'Equipment').

        Returns:
        item : Item
            Returns the item for the player to equip. Returns None if it chose
            a non-equipable object.
        '''
        if item_index <= len(self.items):
            item = self.items[item_index- 1]
            if type(item) == Equipment:
                return item
            else:
                print('Please choose an equipable object.')
                return None

    # TODO: Consumible items
    # def use_item(self):
    #     '''
    #     Selects and uses a certain item from inventory (must be type 'Consumable').

    #     Returns:
    #     item : Item
    #         Returns the item for the player to use. Returns None if it chose
    #         a non-consumable object
    #     '''
    #     print('\nWhich item do you want to use? ["0" to Quit]')
    #     self.show_inventory()
    #     i = int(input("> "))
    #     if i == 0:
    #         print('Closing inventory...')
    #         return None
    #     elif i <= len(self.items):
    #         item = self.items[i - 1]
    #         if item.objectType == 'Consumable':
    #             item.amount -= 1
    #             if item.amount <= 0:
    #                 self.items.pop(i - 1)
    #             return item
    #         else:
    #             print('Please choose a consumable object.')
    #             return None

    def decrease_item_amount(self, item, amount):
        '''
        Decreases a certain amount of a certain item in this inventory.
        This was made because of the shop system.

        Parameters:
        item : Item
            Item to decrease the amount from
        amount : int
            Amount to decrease
        '''
        for actualItem in self.items:
            if item.name == actualItem.name:
                actualItem.amount -= amount
                if actualItem.amount <= 0:
                    self.items.remove(actualItem)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def createInventory(inv_json):
    inv = Inventory()
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

    # TODO: Change Object Type to inheritance
    def __init__(self, name, description, amount, individualValue, objectType) -> None:
        self.name = name
        self.description = description
        self.amount = amount
        self.individualValue = individualValue
        self.objectType = objectType

    def drop(self, amount) -> bool:
        '''
        Drops a certain amount of this item. Dropped items can never be recovered.
        '''
        if amount > self.amount:
            return False
        else:
            self.amount -= amount
            return True

    # # TODO: Sell items
    # def sell(self):
    #     '''
    #     Sells a certain amount of this item. Sold items can never be recovered.

    #     Returns:
    #     moneyToReceive : int
    #         Amount of money to receive for selling X amount of this item.
    #     amountToSell : int
    #         Amount of this item to be sold.
    #     '''
    #     if self.amount >= 1:
    #         print('How many do you want to sell?')
    #         amountToSell = int(input("> "))
    #         if amountToSell <= self.amount and amountToSell > 0:
    #             # Items sell for 50% the value they are worth for
    #             moneyToReceive = int(round(self.individualValue * 0.5 * amountToSell))
    #             print(f'Are you sure you want to sell {amountToSell} {self.name} for {moneyToReceive}G? [y/n]')
    #             confirmation = input("> ")
    #             if confirmation == 'y':
    #                 print(f'{amountToSell} {self.name} sold for {moneyToReceive}')
    #                 return moneyToReceive, amountToSell
    #             else:
    #                 pass
    #         else:
    #             print(f'You don\'t have that many {self.name}!')
    #     return 0, 0

    # def create_item(self, amount):
    #     '''
    #     Creates a copy of this item with a custom "amount".
    #     This was added for the shop system.

    #     Parameters:
    #     amount : int
    #         Amount for the created item to have.
    #     '''
    #     return Item(self.name, self.description, amount, self.individualValue, self.objectType)

    def add_to_inventory_player(self, inventory):
        '''
        Adds the item to the player's inventory.

        Parameters:
        inventory : Inventory
            Inventory of the player.
        '''
        amountAdded = self.amount
        self.add_to_inventory(inventory, amountAdded)
        print(f'{amountAdded} {self.name} was added to your inventory!')

    def add_to_inventory(self, inventory, amount):
        '''
        Adds certain amount of this item to an inventory.
        Made specially for the shop system.

        Parameters:
        inventory : Inventory
            Inventory in which the item will be added.
        amount : int
            Amount of the item to add
        '''
        alreadyInInventory = False
        for item in inventory.items:
            if self.name == item.name:
                item.amount += amount
                alreadyInInventory = True
                break
        if not alreadyInInventory:
            self.amount = amount
            inventory.items.append(self)

    def show_info(self):
        '''
        Shows the info of this specific object.

        Returns:
        info : str
            String with amount, name, objectType and individual value of this object.
        '''
        return f'[x{self.amount}] {self.name} ({self.objectType}) - {self.individualValue}G'

    def show_info_trader(self):
        '''
        Shows the info of this specific object.

        Returns:
        info : str
            String with amount, name, objectType and individual value of this object.
        '''
        return f'{self.name} ({self.objectType}) - {self.individualValue}G'
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def createItem(item_json):
    equipable_items = ['Helmet', 'Armor', 'Weapon', 'Accesory']
    if item_json['objectType'] in equipable_items:
        item = Equipment(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'], item_json['statChangeList'])
    elif item_json['objectType'] == 'Potion':
        item = Potion(item_json['name'], item_json['description'], int(item_json['amount']), int(item_json['individualValue']), item_json['objectType'], item_json['stat'], item_json['amountToChange'])
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
    combo : Combo
        Combo this equipment gives access to.
    '''

    def __init__(self, name, description, amount, individual_value, objectType, statChangeList) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.statChangeList = statChangeList
        #self.combo = combo

    def show_info_trader(self):
        return f'{self.name} ({self.objectType}) [{self.show_stats()}] - {self.individualValue}G'

    def show_info(self):
        return f'[x{self.amount}] {self.name} ({self.objectType}) [{self.show_stats()}] - {self.individualValue}G'

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
        for skill in caster.spells:
            if skill.name == self.spell.name:
                alreadyLearnt = True
                break
        if alreadyLearnt:
            print('You already know this spell.')
        else:
            print(f'Using a \"{self.name}\" you have learnt to cast: \"{self.spell.name}\"!')
            caster.spells.append(self.spell)

    def create_item(self, amount):
        return Grimoire(self.name, self.description, amount, self.individualValue, self.objectType, self.spell)