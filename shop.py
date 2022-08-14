import items
import inventory

class Shop:

    def __init__(self):
        self.items_by_area = {1 : items.area1_shop_list, 2 : items.area2_shop_list}

    def show(self, player):
        items_txt = ''
        index = 1
        for item in self.items_by_area[player.currentArea]:
            items_txt += f'{index} - {item.show_info_trader()}\n'
            index += 1
        return items_txt

    def purchasable_items(self, player):
        purchasable_items = []
        for item in self.items_by_area[player.currentArea]:
            purchasable_items.append(item)

        return purchasable_items