import json

import combat
import file_management
import player as player_module
import enemies as enemies_module


class Fight:

    def __init__(self, player, enemy, fight_msg):
        self.player = player
        self.enemy = enemy
        self.fight_msg = fight_msg

    def normal_attack(self):
        enemy_txt = ""
        player_txt = self.player.normal_attack(self.enemy)
        if self.enemy.alive:
            enemy_txt = self.enemy_action()
        return player_txt + enemy_txt

    def skill(self, skill):
        enemy_txt = ""
        player_txt = skill.effect(self.player, self.enemy)
        if self.enemy.alive:
            enemy_txt = self.enemy_action()
        return player_txt + enemy_txt

    def enemy_action(self):
        if not self.enemy.magicAttack:
            enemy_txt = self.enemy.normal_attack(self.player)
        else:
            enemy_txt = self.enemy.magic_attack(self.player)
        if not self.player.alive:
            self.player.inDungeon = False
            file_management.delete_dungeon(self.player.name)
            self.player.money = round(self.player.money / 2)
            combat.fully_heal(self.player)
            combat.fully_recover_mp(self.player)
        return enemy_txt
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def createFight(fight_json):
    fight = Fight(player=player_module.createPlayer(fight_json['player']), enemy=enemies_module.createEnemy(fight_json['enemy']), fight_msg=fight_json['fight_msg'])
    return fight