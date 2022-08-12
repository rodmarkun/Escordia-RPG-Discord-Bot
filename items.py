import inventory

# Enemy loot
no_loot = inventory.Item("", '', 0, 0, "")

    # Area 1 Monsters
item_wolf_fur = inventory.Item("Wolf Fur", "", 1, 7, "Drop")
item_bat_wings = inventory.Item("Bat wings", "", 1, 5, "Drop")
item_dragonfly_wings = inventory.Item("Dragonfly wings", "", 1, 7, "Drop")

# Weapons

    # Shop Area 1
weapon_rustySword = inventory.Equipment('Rusty Sword', '', 1, 20, 'Weapon', {'atk' : 3})
weapon_brokenDagger = inventory.Equipment('Broken Dagger', '', 1, 20, 'Weapon', {'atk' : 1, 'critCh': 5, 'speed' : 1})
weapon_oldStaff = inventory.Equipment('Old Staff', '', 1, 20, 'Weapon', {'matk' : 1, 'maxMp' : 2})

    # Dungeon Area 1
weapon_longsword = inventory.Equipment('Longsword', '', 1, 50, 'Weapon', {'atk' : 6})
weapon_dagger = inventory.Equipment('Dagger', '', 1, 40, 'Weapon', {'atk' : 4, 'critCh' : 10, 'speed': 2})
weapon_staff = inventory.Equipment('Staff', '', 1, 50, 'Weapon', {'atk' : 2, 'matk' : 3, 'maxMp' : 4})

# Armors

    # Shop Area 1
armor_noviceArmor = inventory.Equipment('Novice Armor', '', 1, 25, 'Armor', {'maxHp' : 3, 'def' : 3, 'speed' : 1})
armor_oldRobes = inventory.Equipment('Old Robes', '', 1, 25, 'Armor', {'maxHp' : 2, 'def' : 1, 'mdef' : 2, 'maxMp' : 2})

    # Dungeon Area 1
armor_clothArmor = inventory.Equipment('Cloth Armor', '', 1, 50, 'Armor', {'maxHp' : 5, 'def' : 4, 'speed' : 3})
armor_bronzeArmor = inventory.Equipment('Bronze Armor', '', 1, 60, 'Armor', {'maxHp' : 9, 'def' : 6})
armor_studentRobes = inventory.Equipment('Student Robes', '', 1, 60, 'Armor', {'maxHp' : 3, 'def' : 3, 'mdef' : 3, 'maxMp' : 6})

# Helmets

    # Dungeon Area 1
helmet_bronzeHelmet = inventory.Equipment('Bronze Helmet', '', 1, 30, 'Helmet', {'maxHp' : 2, 'def' : 2})
helmet_studentHat = inventory.Equipment('Student Hat', '', 1, 40, 'Helmet', {'maxHp' : 1, 'def' : 1, 'maxMp' : 3})

# Accesories

    # Dungeon Area 1
acc_copperRing = inventory.Equipment('Copper Ring', '', 1, 40, 'Accesory', {'def' : 2})
acc_crystalRing = inventory.Equipment('Crystal Ring', '', 1, 40, 'Accesory', {'matk' : 1, 'maxMp' : 2})
acc_shapphireRing = inventory.Equipment('Shapphire Ring', '', 1, 150, 'Accesory', {'maxMp' : 10})



# Loot Lists
dungeon_area_1_loot = [weapon_longsword, weapon_dagger, weapon_staff, armor_clothArmor, armor_bronzeArmor, armor_studentRobes, helmet_bronzeHelmet, helmet_studentHat, acc_copperRing, acc_crystalRing, acc_shapphireRing]