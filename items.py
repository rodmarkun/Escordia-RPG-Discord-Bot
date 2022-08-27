import inventory

# Enemy loot
import skills

no_loot = inventory.Item("", '', 0, 0, "")

    # Area 1 Monsters
item_wolf_fur = inventory.Item("Wolf Fur", "", 1, 7, "Material")
item_bat_wings = inventory.Item("Bat wings", "", 1, 5, "Material")
item_dragonfly_wings = inventory.Item("Dragonfly wings", "", 1, 7, "Material")

    # Area 2 Monsters
item_rogue_badge = inventory.Item("Rogue Badge", "", 1, 25, "Material")
item_harpy_feather = inventory.Item("Harpy Feather", "", 1, 18, "Material")
item_earthworm_tooth = inventory.Item("Earthworm tooth", "", 1, 20, "Material")

# Weapons

    # Shop Area 1
weapon_rustySword = inventory.Equipment('Rusty Sword', '', 1, 20, 'Weapon', 'Swords', {'atk' : 3})
weapon_brokenDagger = inventory.Equipment('Broken Dagger', '', 1, 20, 'Weapon', 'Daggers', {'atk' : 1, 'critCh': 5, 'speed' : 1})
weapon_oldStaff = inventory.Equipment('Old Staff', '', 1, 20, 'Weapon', 'Staffs & Scythes', {'matk' : 1, 'maxMp' : 2})

    # Dungeon 01 Area 1
weapon_longsword = inventory.Equipment('Longsword', '', 1, 50, 'Weapon', 'Swords', {'atk' : 6})
weapon_dagger = inventory.Equipment('Dagger', '', 1, 40, 'Weapon', 'Daggers', {'atk' : 4, 'critCh' : 10, 'speed': 2})
weapon_staff = inventory.Equipment('Staff', '', 1, 50, 'Weapon', 'Staffs & Scythes', {'atk' : 2, 'matk' : 3, 'maxMp' : 4})

    # Shop Area 2
weapon_huntingBow = inventory.Equipment('Hunting Bow', '', 1, 110, 'Weapon', 'Bows', {'atk' : 5, 'critCh' : 35, 'speed' : -6})
weapon_battleAxe = inventory.Equipment('Battle Axe', '', 1, 120, 'Weapon', 'Axes & Hammers', {'atk' : 8, 'def' : 2, 'speed' : -1})
weapon_scimitar = inventory.Equipment('Scimitar', '', 1, 120, 'Weapon', 'Swords', {'atk' : 7, 'critCh' : 5, 'speed' : 3})
weapon_priestStaff = inventory.Equipment('Staff', '', 1, 110, 'Weapon', 'Staffs & Scythes', {'atk' : 4, 'matk' : 5, 'maxMp' : 5})

    # Dungeon 02 Area 2
weapon_boneDagger = inventory.Equipment('Bone Dagger', '', 1, 200, 'Weapon', 'Daggers', {'atk' : 8, 'critCh' : 15, 'speed' : 5})
weapon_necromancerStaff = inventory.Equipment('Necromancer Staff', '', 1, 200, 'Weapon', 'Staffs & Scythes', {'atk' : 5, 'matk' : 8, 'maxMp' : 7})
weapon_ancientWarhammer = inventory.Equipment('Ancient Warhammer', '', 1, 220, 'Weapon', 'Axes & Hammers', {'atk' : 12, 'def' : 4, 'speed' : -5, 'critCh' : -10})
weapon_skeletonAxe = inventory.Equipment('Skeleton Axe', '', 1, 200, 'Weapon', 'Axes & Hammers', {'atk' : 10, 'def' : 3, 'speed' : -3})
weapon_lichScythe = inventory.Equipment('Lich Scythe', '', 1, 250, 'Weapon', 'Staffs & Scythes', {'atk' : 9, 'matk' : 6, 'critCh' : 5})

# Armors

    # Shop Area 1
armor_noviceArmor = inventory.Equipment('Novice Armor', '', 1, 25, 'Armor', '', {'maxHp' : 3, 'def' : 3, 'speed' : 1})
armor_oldRobes = inventory.Equipment('Old Robes', '', 1, 25, 'Armor', '', {'maxHp' : 2, 'def' : 1, 'mdef' : 2, 'maxMp' : 2})

    # Dungeon 01 Area 1
armor_clothArmor = inventory.Equipment('Cloth Armor', '', 1, 50, 'Armor', '', {'maxHp' : 5, 'def' : 4, 'speed' : 3})
armor_bronzeArmor = inventory.Equipment('Bronze Armor', '', 1, 60, 'Armor', '', {'maxHp' : 9, 'def' : 6, 'speed' : -2})
armor_studentRobes = inventory.Equipment('Student Robes', '', 1, 60, 'Armor', '', {'maxHp' : 3, 'def' : 3, 'mdef' : 3, 'maxMp' : 6})

    # Shop Area 2
armor_chainmail = inventory.Equipment('Chainmail', '', 1, 140, 'Armor', '', {'maxHp' : 7, 'def' : 8})
armor_priestRobes = inventory.Equipment('Priest Robes', '', 1, 150, 'Armor', '', {'maxHp' : 5, 'def' : 5, 'mdef' : 5, 'maxMp' : 6})
armor_adventurerArmor = inventory.Equipment('Adventurer Armor', '', 1, 140, 'Armor', '', {'maxHp' : 6, 'def' : 6, 'speed' : 8, 'critCh' : 3})

    # Dungeon 02 Area 2
armor_necromancerRobes = inventory.Equipment('Necromancer Robes', '', 1, 210, 'Armor', '', {'maxHp' : 8, 'def' : 6, 'mdef' : 4, 'maxMp' : 8})
armor_skeletonKnightArmor = inventory.Equipment('Skeleton Knight Armor', '', 1, 220, 'Armor', '', {'maxHp' : 10, 'def' : 8, 'speed' : -2})

# Helmets

    # Dungeon 01 Area 1
helmet_bronzeHelmet = inventory.Equipment('Bronze Helmet', '', 1, 60, 'Helmet', '', {'maxHp' : 2, 'def' : 2})
helmet_studentHat = inventory.Equipment('Student Hat', '', 1, 60, 'Helmet', '', {'maxHp' : 1, 'def' : 1, 'maxMp' : 3})

    # Dungeon 02 Area 2
helmet_spikyHelmet = inventory.Equipment('Spiky Helmet', '', 1, 200, 'Helmet', '', {'maxHp' : 4, 'def' : 4, 'critCh' : 2})
helmet_necromancerMask = inventory.Equipment('Necromancer Mask', '', 1, 220, 'Helmet', '', {'maxHp' : 2, 'def' : 3, 'matk' : 2})
helmet_cultistHat = inventory.Equipment('Cultist Hat', '', 1, 220, 'Helmet', '', {'maxHp' : 1, 'def' : 4, 'maxMp' : 5})

# Accessories

    # Dungeon 01 Area 1
acc_copperRing = inventory.Equipment('Copper Ring', '', 1, 60, 'Accessory', '', {'def' : 2})
acc_crystalRing = inventory.Equipment('Crystal Ring', '', 1, 60, 'Accessory', '', {'matk' : 1, 'maxMp' : 2})
acc_shapphireRing = inventory.Equipment('Shapphire Ring', '', 1, 150, 'Accessory', '', {'maxMp' : 10})


    # Dungeon 02 Area 2
acc_necromancerRing = inventory.Equipment('Necromancer Ring', '', 1, 250, 'Accessory', '', {'maxHp' : -2 ,'matk' : 4, 'maxMp' : 3})
acc_thiefBandana = inventory.Equipment('Thief Bandana', '', 1, 220, 'Accessory', '', {'speed' : 3, 'critCh' : 4})

# Potions

    # Shop Area 2
potion_smallHpPotion = inventory.Potion('Small HP Potion', '', 1, 120, 'Potion', 'hp', 15)

# Grimoires

    # Shop Area 1
grimoire_smallFireBall = inventory.Grimoire('Grimoire: Small Fireball', '', 1, 30, 'Grimoire', skills.spellSmallFireball)

    # Dungeon 01 Area 1
grimoire_fireball = inventory.Grimoire('Grimoire: Fireball', '', 1, 120, 'Grimoire', skills.spellFireball)
grimoire_smallBlessing = inventory.Grimoire('Grimoire: Small Blessing', '', 1, 130, 'Grimoire', skills.spellSmallBlessing)

# Shop Lists
    # Area 1
area1_shop_list = [weapon_rustySword, weapon_brokenDagger, weapon_oldStaff, armor_noviceArmor, armor_oldRobes, grimoire_smallFireBall]
area2_shop_list = [weapon_huntingBow, weapon_scimitar, weapon_battleAxe, weapon_priestStaff, armor_chainmail, armor_priestRobes, armor_adventurerArmor, helmet_bronzeHelmet, helmet_studentHat, acc_copperRing, acc_crystalRing, potion_smallHpPotion, grimoire_fireball]

# Loot Lists
dungeon_area_1_loot = [weapon_longsword, weapon_dagger, weapon_staff, armor_clothArmor, armor_bronzeArmor, armor_studentRobes, helmet_bronzeHelmet, helmet_studentHat, acc_copperRing, acc_crystalRing, acc_shapphireRing, grimoire_fireball, grimoire_smallBlessing]
dungeon_area_2_loot = [weapon_boneDagger, weapon_necromancerStaff, weapon_ancientWarhammer, weapon_skeletonAxe, weapon_lichScythe, armor_necromancerRobes, armor_skeletonKnightArmor, helmet_spikyHelmet, helmet_necromancerMask, helmet_cultistHat, acc_necromancerRing, acc_thiefBandana, potion_smallHpPotion, grimoire_smallBlessing]