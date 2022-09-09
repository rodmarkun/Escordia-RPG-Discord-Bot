import emojis
import items

def show_crafting_recipes(tier, player_obj):
    recipe_txt = ""
    for recipe in all_recipes[tier-1]:
        recipe_txt += f'**Item**: `{recipe["craft"].name.lower().replace(" ", "_")}` {recipe["craft"].show_info_trader()}\n**Materials Needed:** '
        i = 0
        for item in recipe["items"]:
            recipe_txt += f'{item.emoji} x{recipe["quantity"][i]} {item.name} '
            i += 1
        all_materials_needed = True
        i = 0
        for item in recipe["items"]:
            if not player_obj.inventory.check_for_item_and_amount(item.name, recipe["quantity"][i]):
                all_materials_needed = False
            i += 1
        if all_materials_needed:
            recipe_txt += f" {emojis.CHECK_EMOJI}"
        else:
            recipe_txt += f" {emojis.CROSS_EMOJI}"
        recipe_txt += "\n\n"
    recipe_txt += "\nType `!craft [item_name]` to craft an item. Use the highlighted item name above. For example: `!craft bronze_armor`."
    return recipe_txt

recipes_tier1 = [{"craft" : items.weapon_longsword, "items" : [items.gathering_oakWood, items.gathering_tin], "quantity" : [3, 2]},
                 {"craft" : items.weapon_dagger, "items" : [items.gathering_oakWood, items.gathering_copper], "quantity" : [2, 2]},
                 {"craft" : items.weapon_staff, "items" : [items.gathering_oakWood, items.gathering_copper, items.gathering_tin], "quantity" : [2, 1, 1]},
                 {"craft" : items.armor_clothArmor, "items" : [items.item_insect_cloth, items.item_bat_wings], "quantity" : [3, 1]},
                 {"craft" : items.armor_studentRobes, "items" : [items.item_insect_cloth], "quantity" : [4]},
                 {"craft" : items.armor_bronzeArmor, "items" : [items.gathering_tin, items.gathering_copper], "quantity" : [2, 3]},
                 {"craft" : items.helmet_wolfHelmet, "items" : [items.item_insect_cloth, items.item_wolf_fur], "quantity" : [1, 2]},
                 {"craft" : items.acc_copperRing, "items" : [items.gathering_copper], "quantity" : [2]}
                 ]
recipes_tier2 = [{"craft" : items.weapon_huntingBow, "items" : [items.gathering_cedarWood, items.item_insect_cloth, items.item_harpy_feather], "quantity" : [3, 2, 2]},
                 {"craft" : items.weapon_broadsword, "items" : [items.gathering_mapleWood, items.gathering_iron], "quantity" : [2, 5]},
                 {"craft" : items.weapon_ancientWarhammer, "items" : [items.gathering_mapleWood, items.gathering_brass], "quantity" : [3, 4]},
                 {"craft" : items.armor_chainmail, "items" : [items.gathering_iron, items.gathering_brass, items.item_rogue_cloth], "quantity" : [3, 2, 2]},
                 {"craft" : items.armor_rogueArmor, "items" : [items.item_rogue_cloth, items.item_harpy_feather], "quantity" : [5, 1]},
                 {"craft" : items.helmet_ironHelmet, "items" : [items.gathering_iron, items.item_rogue_cloth], "quantity" : [3, 1]},
                 {"craft" : items.helmet_cultistHat, "items" : [items.item_rogue_cloth, items.item_earthworm_tooth], "quantity" : [2, 2]},
                 {"craft" : items.acc_thiefBandana, "items" : [items.item_rogue_cloth, items.item_harpy_feather], "quantity" : [3, 1]},
                 {"craft" : items.acc_smallWand, "items" : [items.gathering_cedarWood, items.item_earthworm_tooth], "quantity" : [2, 1]},
                 {"craft" : items.acc_ironRing, "items" : [items.gathering_iron, items.gathering_brass], "quantity" : [2, 2]},
                 ]
all_recipes = [recipes_tier1, recipes_tier2]