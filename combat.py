import random
import math
import inventory

'''
Parent class for all instances that can enter in combat.
A Battler will always be either an Enemy, a Player's ally or the Player himself
'''
class Battler:
    '''
    Parent class for all instances that can enter in combat.
    A Battler will always be either an Enemy, a Player's ally or the Player himself
    '''
    def __init__(self, name, stats) -> None:
        '''
        Creates a new battler

        :param name: Name of the battler.
        :param stats: Stats of the battler in dictionary format. Ex: {'atk' : 3}.
        '''
        self.name = name
        self.stats = stats
        self.alive = True
        self.buffsAndDebuffs = []
        self.isAlly = False

    def take_dmg(self, dmg):
        '''
        Function for battlers taking damage from any source.
        Subtracts the damage quantity from its health. Also checks if it dies.

        :param dmg: Damage about to be taken by battler
        :return: Info about damage taken
        '''
        if dmg < 0: dmg = 0
        self.stats['hp'] -= dmg
        info_dmg = f'{self.name} takes {dmg} damage!\n'
        # Defender dies
        if self.stats['hp'] <= 0:
            info_dmg += f'{self.name} has been slain.\n'
            self.alive = False
        return info_dmg

    def normal_attack(self, defender):
        '''
        Normal attack all battlers have.

        Damage is calculated as follows:
        attacker_atk * (100/(100 + defender_def * 2.5))

        :param defender: Defending battler
        :return: Attack info string
        '''
        info = f'{self.name} attacks!\n'
        info_crit = ""
        info_miss = ""
        info_dmg = ""
        dmg = round(self.stats['atk'] * (100/(100 + defender.stats['def']*2.5)))
        # Check for critical attack
        #dmg, info_crit = self.check_critical(dmg)
        if self.check_critical():
            info_crit = 'Critical blow!\n'
            dmg = round(dmg * 1.5)
        # Check for missed attack
        if not check_miss(self, defender):
            info_dmg = defender.take_dmg(dmg)
        else:
            info_miss = f'{self.name}\'s attack missed!\n'
        return info + info_crit + info_miss + info_dmg

    def magic_attack(self, defender):
        '''
        Magic attacks mage enemies perform.
        They cannot be evaded.

        :param defender: Defending battler
        :return: Attack info string
        '''
        info = f'{self.name} performs a magic attack!\n'
        info_miss = ""
        dmg = round(self.stats['matk'] * (100 / (100 + defender.stats['mdef'] * 1.5)))

        info_dmg = defender.take_dmg(dmg)
        return info + info_miss + info_dmg

    def check_critical(self):
        '''
        Checks if an attack is critical. If it is, increments its damage.

        Critical chance comes by the battler's stat: 'critCh'
        '''
        return self.stats['critCh'] > random.randint(0, 100)

    def recover_mp(self, amount):
        '''
        Battler recovers certain amount of 'mp' (Mana Points).

        :param amount: Amount of MP recovered
        '''
        if self.stats['mp'] + amount > self.stats['maxMp']:
            fully_recover_mp(self)
        else:
            self.stats['mp'] += amount

    def heal(self, amount):
        '''
        Battler recovers certain amount of 'hp' (Health Points).

        :param amount: Amount of HP recovered
        '''
        if self.stats['hp'] + amount > self.stats['maxHp']:
            fully_heal(self)
        else:
            self.stats['hp'] += amount

def check_miss(attacker, defender):
    '''
    Checks if an attack misses or not. Miss chance is determined by the following formula:

    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))

    I tried different formulas and this one ended up being pretty competent. Check if
    it fits you anyway.

    :param attacker: Attacking Battler
    :param defender: Defending Battler
    :return: True if attack misses. False if it does not.
    '''
    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))
    return chance > random.randint(0, 100)

def check_turns_buffs_and_debuffs(target, deactivate):
    '''
    Checks if buffs and debuffs should still be active (checks its turn count).

    :param target: Battler whose buffs and debuffs should be checked
    :param deactivate: If true, buffs and debuffs deactivate instantly regardless of turn count
        (useful when ending a combat or any similar situation). If false, acts
        normally.
    '''
    if deactivate:
        for bd in target.buffsAndDebuffs:
            bd.deactivate()
    else:
        for bd in target.buffsAndDebuffs:
            bd.check_turns()

def fully_heal(target):
    '''
    Fully heals a target

    :param target: Target battler
    '''
    target.stats['hp'] = target.stats['maxHp']

def fully_recover_mp(target):
    '''
    Fully recovers target's MP

    :param target: Target battler
    '''
    target.stats['mp'] = target.stats['maxMp']

def check_if_loot(player, enemy):
    '''
    Checks if player gets to loot the enemy

    :param player: Player that slain the enemy
    :param enemy: Enemy to loot
    :return: True/False whether the player gets to loot the enemy or not
    '''
    if random.randint(0, 100) <= enemy.lootChance:
        player.inventory.add_item(inventory.createItem(enemy.possibleLoot))
        return True
    else:
        return False