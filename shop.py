import items
import emojis

class Shop:

    def __init__(self):
        self.items_by_area = {1 : items.area1_shop_list, 2 : items.area2_shop_list}

    def show(self, player):
        items_txt = ''
        index = 1
        for item in self.items_by_area[player.currentArea]:
            if item.objectType != 'Weapon':
                items_txt += f'{index} - {emojis.obj_to_emoji[item.objectType]} {item.show_info_trader()}\n'
            else:
                items_txt += f'{index} - {emojis.weapon_to_emoji[item.objectSubType]} {item.show_info_trader()}\n'
            index += 1
        return items_txt

    def purchasable_items(self, player):
        purchasable_items = []
        for item in self.items_by_area[player.currentArea]:
            purchasable_items.append(item)

        return purchasable_items