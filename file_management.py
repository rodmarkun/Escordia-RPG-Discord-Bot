import json
import dungeons
import inventory
import player
import time
import fight as fight_module
import skills


def check_if_exists(player_name):
    '''
    Checks if a player exists in "players.txt"

    :param player_name: Name of the player to search
    :return: Player object if found, None if not found
    '''

    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['name'] == player_name:
                player_obj = player.createPlayer(res)
    with open("inventory.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['player_name'] == player_name:
                player_obj.inventory = inventory.createInventory(res)
                return player_obj
    return None

def write_fight(fight_obj):
    '''
    Writes a new Fight object into "fights.txt"
    :param fight_obj: Fight object to be written
    '''
    with open("fights.txt", "a") as file:
        file.write(fight_obj.toJSON() + '\n')

def delete_fight(player_name):
    '''
    Deletes an existing fight in which a player is involved

    :param player_name: Name of the player whose fight is about to be deleted
    '''
    with open("fights.txt", "r") as file:
        lines = file.readlines()
    with open("fights.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['player']['name'] != player_name:
                file.write(line)

def check_if_in_fight(player_name):
    '''
    Checks if a certain player is currently involved in a fight

    :param player_name: Name of the player to search
    :return: Fight object from "fights.txt"
    '''
    with open("fights.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['player']['name'] == player_name:
                return fight_module.createFight(res)
    return None

def write_dungeon(dungeon_obj):
    '''
    Writes a dungeon into "dungeons.txt"

    :param dungeon_obj: Dungeon object to be written
    '''
    with open("dungeons.txt", "a") as file:
        file.write(dungeon_obj.toJSON() + '\n')

def delete_dungeon(player_name):
    '''
    Deletes a dungeon object from "dungeons.txt"

    :param player_name: Player who is currently fighting in the dungeon
    '''
    with open("dungeons.txt", "r") as file:
        lines = file.readlines()
    with open("dungeons.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['player_name'] != player_name:
                file.write(line)

def check_if_in_dungeon(player_name):
    '''
    Checks if a certain player is currently inside a dungeon from "dungeons.txt"

    :param player_name: Name of the player to search
    :return: Dungeon object if found, None if not found
    '''
    with open("dungeons.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['player_name'] == player_name:
                return dungeons.createDungeon(res)
    return None

def write_player(player_obj):
    '''
    Writes a new player into "players.txt"

    :param player_obj: Player object about to be written
    '''
    with open("players.txt", "a") as file:
        file.write(player_obj.toJSON() + '\n')
    write_inventory(player_obj)
    create_masteries(player_obj)

def delete_player(player_name):
    '''
    Deletes a player object from "players.txt"

    :param player_name: Name of the player to be deleted
    '''
    with open("players.txt", "r") as file:
        lines = file.readlines()
    with open("players.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['name'] != player_name:
                file.write(line)
    delete_inventory(player_name)

def write_inventory(player_obj):
    '''
    Writes a new inventory object from a certain player into "inventory.txt"

    :param player_obj: Player object which contains the Inventory object
    '''
    print(player_obj.inventory)
    print(player_obj.inventory.toJSON())
    with open("inventory.txt", "a") as file:
        file.write(player_obj.inventory.toJSON() + '\n')

def delete_inventory(player_name):
    '''
    Deletes the inventory of a certain player

    :param player_name: Player name whose inventory is about to be deleted
    '''
    with open("inventory.txt", "r") as file:
        lines = file.readlines()
    with open("inventory.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['player_name'] != player_name:
                file.write(line)

def get_inventory(player_name):
    with open("inventory.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            res = json.loads(line)
            if res['player_name'] == player_name:
                return inventory.createInventory(res)

def update_player(player_obj):
    '''
    Updates player with all the necessary information. Needed each time the Player object changes.

    :param player_obj: Player object to be updated
    '''
    with open("players.txt", "r") as file:
        lines = file.readlines()
    with open("players.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['name'] != player_obj.name:
                file.write(line)
            else:
                file.write(player_obj.toJSON() + '\n')
    delete_inventory(player_obj.name)
    write_inventory(player_obj)

def create_masteries(player_obj):
    '''
    Creates an entry for a player's masteries

    :param player_obj:
    '''
    with open("masteries.txt", "a") as file:
        masteries_dict = {"name" : player_obj.name, "masteries" : player.masteries}
        file.write(json.dumps(masteries_dict) + '\n')

def update_masteries(player_obj, weapon, exp):
    with open("masteries.txt", "r") as file:
        lines = file.readlines()
    with open("masteries.txt", "w") as file:
        for line in lines:
            print(line)
            res = json.loads(line)
            if res['name'] != player_obj.name:
                file.write(line)
            else:
                info_txt = ""
                masteries_dict = res["masteries"]
                masteries_dict[weapon]["xp"] += exp
                while masteries_dict[weapon]["xp"] > masteries_dict[weapon]["xpToNextLvl"]:
                    masteries_dict[weapon]["lvl"] += 1
                    masteries_dict[weapon]["xp"] -= masteries_dict[weapon]["xpToNextLvl"]
                    masteries_dict[weapon]["xpToNextLvl"] = round(masteries_dict[weapon]["xpToNextLvl"] * 1.5 + 100 * masteries_dict[weapon]["lvl"] * masteries_dict[weapon]["lvl"] / 2)
                    try:
                        player_obj.combos.append(skills.combo_learn[weapon][masteries_dict[weapon]["lvl"]])
                    except:
                        print("Something went wrong when learning a new combo")
                    info_txt += f"Your mastery with {weapon} has leveled up! You have acquired a new combo!\n"
                res["masteries"] = masteries_dict
                file.write(json.dumps(res) + '\n')
                return info_txt

def get_masteries(player_obj):
    with open("masteries.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['name'] == player_obj.name:
                return res

def get_all_players():
    players_string = ''
    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            players_string += res['name'] + '\n'
    return players_string

