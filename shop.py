import items

class Shop:
    '''
    Class which stores all information regarding the shops across all areas.
    '''

    def __init__(self):
        '''
        Creates a new shop.
        '''
        self.items_by_area = {1 : items.area1_shop_list, 2 : items.area2_shop_list}

    def show(self, player):
        '''
        Shows all items stored in the shop.

        :param player: Player object
        :return: Items string
        '''
        items_txt = ''
        index = 1
        for item in self.items_by_area[player.currentArea]:
            if item.objectType != 'Weapon':
                items_txt += f'{index} - {item.show_info_trader()}\n'
            else:
                items_txt += f'{index} - {item.show_info_trader()}\n'
            index += 1
        return items_txt

    def purchasable_items(self, player):
        '''
        Gets all items that can be currently purchased by the player

        :param player: Player obj
        :return: Item list containing all purchasable items
        '''
        purchasable_items = []
        for item in self.items_by_area[player.currentArea]:
            purchasable_items.append(item)

        return purchasable_items