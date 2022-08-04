import json
import player as player_module
import enemies as enemies_module


class Fight:

    def __init__(self, player, enemy, fight_msg):
        self.player = player
        self.enemy = enemy
        self.fight_msg = fight_msg

    def normal_attack(self):
        self.player.normal_attack(self.enemy)
        if self.enemy.alive:
            self.enemy.normal_attack(self.player)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def createFight(fight_json):
    fight = Fight(player=player_module.createPlayer(fight_json['player']), enemy=enemies_module.createEnemy(fight_json['enemy']), fight_msg=fight_json['fight_msg'])
    return fight