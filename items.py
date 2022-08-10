import inventory

# Enemy loot
no_loot = inventory.Item("", '', 0, 0, "")
item_wolf_fur = inventory.Item("Wolf Fur", "", 1, 7, "Drop")
item_bat_wings = inventory.Item("Bat wings", "", 1, 5, "Drop")
item_dragonfly_wings = inventory.Item("Dragonfly wings", "", 1, 7, "Drop")

# Weapons
longsword = inventory.Equipment('Longsword', '', 1, 19, 'Weapon', {'atk' : 6, 'def' : 2})
dagger = inventory.Equipment('Dagger', '', 1, 15, 'Weapon', {'atk' : 4, 'critCh' : 10, 'speed': 2})