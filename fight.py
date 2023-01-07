import json

import combat
import file_management
import player as player_module
import enemies as enemies_module


class Fight:
    '''
    Stores information of an ongoing fight.
    '''

    def __init__(self, player, enemy):
        '''
        Creates a new fight

        :param player: Player fighting
        :param enemy: Enemy being fighted
        :param fight_msg: Discord message ID from fight command. Deprecated, is not used.
        '''
        self.player = player
        self.enemy = enemy

    def normal_attack(self):
        '''
        Player performs a normal attack.

        :return: Normal attack info string.
        '''
        enemy_txt = ""
        player_txt = self.player.normal_attack(self.enemy)
        if self.enemy.alive:
            enemy_txt = self.enemy_action()
        return player_txt + enemy_txt

    def skill(self, skill):
        '''
        Player performs a skill.

        :param skill: Skill performed by the player.
        :return: Skill info string
        '''
        enemy_txt = ""
        player_txt = skill.effect(self.player, self.enemy)
        if self.enemy.alive:
            enemy_txt = self.enemy_action()
        return player_txt + enemy_txt

    def enemy_action(self):
        '''
        Enemy's AI (Can be very further expanded)

        :return: Enemy action info string
        '''
        if not self.enemy.magicAttack:
            enemy_txt = self.enemy.normal_attack(self.player)
        else:
            enemy_txt = self.enemy.magic_attack(self.player)
        if not self.player.alive: self.player.death()
        return enemy_txt

    def toJSON(self):
        '''
        Transforms a fight instance into a JSON

        :return: Fight JSON
        '''
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def createFight(fight_json):
    '''
    Creates a fight instance from a JSON

    :param fight_json: Fight JSON
    :return: Fight instance
    '''
    fight = Fight(player=player_module.createPlayer(fight_json['player']), enemy=enemies_module.createEnemy(fight_json['enemy']))
    return fight