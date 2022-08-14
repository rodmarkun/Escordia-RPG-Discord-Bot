import json
import dungeons
import player
import time
import fight as fight_module

def check_if_exists(player_name):
    start_time = time.time() * 1000
    with open("players.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['name'] == player_name:
                end_time = time.time() * 1000
                print(f'CHECK_IF_EXISTS TIME: {start_time-end_time}')
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
    start_time = time.time() * 1000
    with open("fights.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['player']['name'] == player_name:
                end_time = time.time() * 1000
                print(f'CHECK_IF_IN_FIGHT TIME: {end_time - start_time}')
                return fight_module.createFight(res)
    return None

def delete_dungeon(player_name):
    with open("dungeons.txt", "r") as file:
        lines = file.readlines()
    with open("dungeons.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['player_name'] != player_name:
                file.write(line)

def write_dungeon(dungeon_obj):
    with open("dungeons.txt", "a") as file:
        file.write(dungeon_obj.toJSON() + '\n')

def check_if_in_dungeon(player_name):
    with open("dungeons.txt", "r") as file:
        for line in file:
            res = json.loads(line)
            if res['player_name'] == player_name:
                return dungeons.createDungeon(res)
    return None

def delete_player(player_name):
    start_time = time.time() * 1000
    with open("players.txt", "r") as file:
        lines = file.readlines()
    with open("players.txt", "w") as file:
        for line in lines:
            res = json.loads(line)
            if res['name'] != player_name:
                file.write(line)
    end_time = time.time() * 1000
    print(f'DELETE_PLAYER TIME: {end_time - start_time}')

def write_player(player_obj):
    start_time = time.time() * 1000
    with open("players.txt", "a") as file:
        file.write(player_obj.toJSON() + '\n')
    end_time = time.time() * 1000
    print(f'WRITE_PLAYER TIME: {end_time - start_time}')