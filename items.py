import inventory
import skills


# No Loot

no_loot = inventory.Item("", '', 0, 0, "")

# Area 1
    # Materials
item_wolf_fur = inventory.Item("Wolf Fur", "", 1, 8, "Material")
item_bat_wings = inventory.Item("Bat wings", "", 1, 6, "Material")
item_insect_cloth = inventory.Item("Insect Cloth", "", 1, 8, "Material")
    # Weapons
weapon_rustySword = inventory.Equipment('Rusty Sword', '', 1, 20, 'Weapon', 'Swords', {'atk' : 3})
weapon_brokenDagger = inventory.Equipment('Broken Dagger', '', 1, 20, 'Weapon', 'Daggers', {'atk' : 1, 'critCh': 5, 'speed' : 1})
weapon_oldStaff = inventory.Equipment('Old Staff', '', 1, 20, 'Weapon', 'Staffs & Scythes', {'atk' : 1,'matk' : 1, 'maxMp' : 2})

weapon_longsword = inventory.Equipment('Longsword', '', 1, 50, 'Weapon', 'Swords', {'atk' : 6})
weapon_dagger = inventory.Equipment('Dagger', '', 1, 40, 'Weapon', 'Daggers', {'atk' : 4, 'critCh' : 10, 'speed': 2})
weapon_staff = inventory.Equipment('Staff', '', 1, 50, 'Weapon', 'Staffs & Scythes', {'atk' : 2, 'matk' : 3, 'maxMp' : 4})
    # Armor
armor_noviceArmor = inventory.Equipment('Novice Armor', '', 1, 25, 'Armor', '', {'maxHp' : 3, 'def' : 3, 'speed' : 1})
armor_oldRobes = inventory.Equipment('Old Robes', '', 1, 25, 'Armor', '', {'maxHp' : 2, 'def' : 1, 'mdef' : 2, 'maxMp' : 2})

armor_clothArmor = inventory.Equipment('Cloth Armor', '', 1, 50, 'Armor', '', {'maxHp' : 5, 'def' : 4, 'speed' : 3})
armor_bronzeArmor = inventory.Equipment('Bronze Armor', '', 1, 60, 'Armor', '', {'maxHp' : 9, 'def' : 6, 'speed' : -2})
armor_studentRobes = inventory.Equipment('Student Robes', '', 1, 60, 'Armor', '', {'maxHp' : 3, 'def' : 3, 'mdef' : 3, 'maxMp' : 6})
    # Helmet
helmet_wolfHelmet = inventory.Equipment('Wolf Helmet', '', 1, 40, 'Helmet', '', {'maxHp' : 2, 'speed' : 1})

helmet_bronzeHelmet = inventory.Equipment('Bronze Helmet', '', 1, 60, 'Helmet', '', {'maxHp' : 2, 'def' : 2})
helmet_studentHat = inventory.Equipment('Student Hat', '', 1, 60, 'Helmet', '', {'maxHp' : 1, 'def' : 1, 'maxMp' : 3})
    # Accessory
acc_copperRing = inventory.Equipment('Copper Ring', '', 1, 60, 'Accessory', '', {'def' : 2})
acc_crystalRing = inventory.Equipment('Crystal Ring', '', 1, 60, 'Accessory', '', {'matk' : 1, 'maxMp' : 2})
acc_shapphireRing = inventory.Equipment('Shapphire Ring', '', 1, 150, 'Accessory', '', {'maxMp' : 10})
    # Grimoire
grimoire_smallFireBall = inventory.Grimoire('Grimoire: Small Fireball', '', 1, 30, 'Grimoire', skills.spellSmallFireball)
grimoire_smallBlessing = inventory.Grimoire('Grimoire: Small Blessing', '', 1, 130, 'Grimoire', skills.spellSmallBlessing)



# Area 2
    # Materials
item_rogue_cloth = inventory.Item("Rogue Cloth", "", 1, 25, "Material")
item_harpy_feather = inventory.Item("Harpy Feather", "", 1, 18, "Material")
item_earthworm_tooth = inventory.Item("Earthworm tooth", "", 1, 20, "Material")
    # Weapons
weapon_battleAxe = inventory.Equipment('Battle Axe', '', 1, 120, 'Weapon', 'Axes & Hammers', {'atk' : 8, 'def' : 2, 'speed' : -2})
weapon_scimitar = inventory.Equipment('Scimitar', '', 1, 120, 'Weapon', 'Swords', {'atk' : 6, 'critCh' : 5, 'speed' : 3})
weapon_priestStaff = inventory.Equipment('Staff', '', 1, 110, 'Weapon', 'Staffs & Scythes', {'atk' : 4, 'matk' : 5, 'maxMp' : 5})

weapon_huntingBow = inventory.Equipment('Hunting Bow', '', 1, 180, 'Weapon', 'Bows', {'atk' : 6, 'critCh' : 30, 'speed' : -5})
weapon_broadsword = inventory.Equipment('Broadsword', '', 1, 180, 'Weapon', 'Swords', {'atk' : 12, 'def' : -2, 'speed' : -2})
weapon_ancientWarhammer = inventory.Equipment('Ancient Warhammer', '', 1, 180, 'Weapon', 'Axes & Hammers', {'atk' : 10, 'def' : 4, 'speed' : -3, 'critCh' : -5})

weapon_boneDagger = inventory.Equipment('Bone Dagger', '', 1, 200, 'Weapon', 'Daggers', {'atk' : 9, 'critCh' : 12, 'speed' : 3})
weapon_necromancerStaff = inventory.Equipment('Necromancer Staff', '', 1, 200, 'Weapon', 'Staffs & Scythes', {'maxHp' : -2,'atk' : 7, 'matk' : 8, 'maxMp' : 8})
weapon_lichScythe = inventory.Equipment('Lich Scythe', '', 1, 250, 'Weapon', 'Staffs & Scythes', {'atk' : 12, 'matk' : 8, 'critCh' : 5})

weapon_antKnightSting = inventory.Equipment('Ant Knight Sting', '', 1, 240, 'Weapon', 'Swords', {'atk' : 11, 'critCh' : 5, 'speed' : 4})
weapon_blackAntBow = inventory.Equipment('Black Ant Bow', '', 1, 240, 'Weapon', 'Bows', {'atk' : 9, 'critCh' : 18, 'speed' : -4})
    # Armors
armor_chainmail = inventory.Equipment('Chainmail', '', 1, 150, 'Armor', '', {'maxHp' : 13, 'def' : 8, 'mdef' : 2})
armor_rogueArmor = inventory.Equipment('Rogue Armor', '', 1, 150, 'Armor', '', {'maxHp' : 9, 'def' : 6, 'mdef' : 3, 'speed' : 3})

armor_necromancerRobes = inventory.Equipment('Necromancer Robes', '', 1, 180, 'Armor', '', {'maxHp' : 8, 'def' : 5, 'mdef' : 4, 'maxMp' : 8})

armor_blackProtectorBreastplate = inventory.Equipment('Black Protector Breastplate', '', 1, 350, 'Armor', '', {'maxHp' : 16, 'def' : 10, 'mdef' : 7, 'speed' : -1})
armor_antQueenMantle = inventory.Equipment('Ant Queen Mantle', '', 1, 350, 'Armor', '', {'maxHp' : 10, 'def' : 8, 'mdef' : 9, 'maxMp' : 10})
    # Helmets
helmet_ironHelmet = inventory.Equipment('Iron Helmet', '', 1, 190, 'Helmet', '', {'maxHp' : 5, 'def' : 3, 'mdef' : 2})
helmet_cultistHat = inventory.Equipment('Cultist Hat', '', 1, 190, 'Helmet', '', {'maxHp' : 3, 'def' : 2, 'mdef' : 2, 'maxMp' : 3})

helmet_spikyHelmet = inventory.Equipment('Spiky Helmet', '', 1, 220, 'Helmet', '', {'maxHp' : 5, 'def' : 5, 'atk' : 3})
    # Accessories
acc_thiefBandana = inventory.Equipment('Thief Bandana', '', 1, 220, 'Accessory', '', {'def' : 2, 'speed' : 3, 'critCh' : 4})
acc_smallWand = inventory.Equipment('Small Wand', '', 1, 220, 'Accessory', '', {'matk' : 5, 'maxMp' : 2})
acc_ironRing = inventory.Equipment('Iron Ring', '', 1, 220, 'Accessory', '', {'def' : 4, 'mdef' : 1})

acc_skeletonRing = inventory.Equipment('Skeleton Ring', '', 1, 250, 'Accessory', '', {'maxHp' : -4 ,'def' : 7})
acc_antiqueOrb = inventory.Equipment('Antique Orb', '', 1, 250, 'Accessory', '', {'def' : 3, 'mdef' : 3, 'maxMp' : 7})
acc_heroCape = inventory.Equipment('Hero Cape', '', 1, 250, 'Accessory', '', {'atk' : 3,'def' : 3, 'speed' : 2})
    # Potions
potion_smallHpPotion = inventory.Potion('Small HP Potion', '', 1, 120, 'Potion', 'hp', 15)
    # Grimoires
grimoire_fireball = inventory.Grimoire('Grimoire: Fireball', '', 1, 120, 'Grimoire', skills.spellFireball)

# Gathering

    # Tools
gathering_simpleGatheringPickaxe = inventory.Equipment("Simple Gathering Pickaxe", '', 1, 30, "Pickaxe", "Gathering", {'miningTier' : 1})
gathering_simpleGatheringAxe = inventory.Equipment("Simple Gathering Axe", '', 1, 30, "Axe", "Gathering", {'choppingTier' : 1})

gathering_bronzeGatheringPickaxe = inventory.Equipment("Bronze Gathering Pickaxe", '', 1, 100, "Pickaxe", "Gathering", {'miningTier' : 2})
gathering_bronzeGatheringAxe = inventory.Equipment("Bronze Gathering Axe", '', 1, 100, "Axe", "Gathering", {'choppingTier' : 2})
    # Tier 1
gathering_oakWood = inventory.Item("Oak Wood", '', 1, 10, 'Wood')
gathering_copper = inventory.Item("Copper", '', 1, 10, 'Ore')
gathering_tin = inventory.Item("Tin", '', 1, 10, 'Ore')

gathering_cedarWood = inventory.Item("Cedar Wood", '', 1, 25, 'Wood')
gathering_mapleWood = inventory.Item("Maple Wood", '', 1, 25, 'Wood')
gathering_iron = inventory.Item("Iron", '', 1, 25, 'Ore')
gathering_brass = inventory.Item("Brass", '', 1, 25, 'Ore')

# Gathering Nodes

gathering_nodes = {"mining" : [[gathering_copper, gathering_tin], [gathering_iron, gathering_brass]], "chopping" : [[gathering_oakWood], [gathering_cedarWood, gathering_mapleWood]]}

# Shop Lists
    # Area 1
area1_shop_list = [weapon_rustySword, weapon_brokenDagger, weapon_oldStaff, armor_noviceArmor, armor_oldRobes, grimoire_smallFireBall, gathering_simpleGatheringPickaxe, gathering_simpleGatheringAxe]
area2_shop_list = [weapon_battleAxe, weapon_scimitar, weapon_priestStaff, potion_smallHpPotion, grimoire_fireball, gathering_bronzeGatheringPickaxe, gathering_bronzeGatheringAxe]

# Loot Lists
dungeon_area_1_loot = [helmet_bronzeHelmet, helmet_studentHat, acc_crystalRing, acc_shapphireRing, grimoire_smallBlessing]
dungeon_area_2_loot = [weapon_boneDagger, weapon_necromancerStaff, armor_necromancerRobes, acc_skeletonRing, helmet_spikyHelmet, weapon_lichScythe, grimoire_fireball]
dungeon_area_3_loot = [weapon_antKnightSting, weapon_blackAntBow, acc_antiqueOrb, acc_heroCape, armor_blackProtectorBreastplate, armor_antQueenMantle]