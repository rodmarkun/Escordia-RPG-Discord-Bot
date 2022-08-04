import json
import player
import fight as fight_module

def check_if_exists(player_name):
    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['name'] == player_name:
                return player.createPlayer(res)
    return None

def delete_fight(player_name):
    with open("fights.txt", "r") as file:
        lines = file.readlines()
    with open("fights.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['player']['name'] != player_name:
                file.write(line)

def write_fight(fight_obj):
    with open("fights.txt", "a") as file:
        file.write(fight_obj.toJSON() + '\n')

def check_if_in_fight(player_name):
    with open("fights.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['player']['name'] == player_name:
                return fight_module.createFight(res)
    return None

def delete_player(player_name):
    with open("players.txt", "r") as file:
        lines = file.readlines()
    with open("players.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['name'] != player_name:
                file.write(line)

def write_player(player_obj):
    with open("players.txt", "a") as file:
        file.write(player_obj.toJSON() + '\n')