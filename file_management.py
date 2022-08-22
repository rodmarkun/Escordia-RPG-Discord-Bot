import json
import dungeons
import inventory
import player
import time
import fight as fight_module

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