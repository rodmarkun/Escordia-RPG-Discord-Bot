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

    Attributes:
    name : str
        Name of the battler.
    stats : dict
        Stats of the battler, dictionary ex: {'atk' : 3}.
    alive : bool
        Bool for battler being alive or dead.
    buffsAndDebuffs : list
        List of buffs and debuffs battler currently has.
    isAlly : bool
        Bool for battler being a Player's ally or not.
    '''
    def __init__(self, name, stats) -> None:
        self.name = name
        self.stats = stats
        self.alive = True
        self.buffsAndDebuffs = []
        self.isAlly = False

    def take_dmg(self, dmg):
        '''
        Function for battlers taking damage from any source.
        Subtracts the damage quantity from its health. Also checks if it dies.

        Parameters:
        dmg : int
            Quantity of damage dealt
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
        attacker_atk * (100/(100 + defender_def * 1.5))

        Parameters:
        defender : Battler
            Defending battler

        Returns:
        dmg : int
            Damage dealt to defender
        '''
        info = f'{self.name} attacks!\n'
        info_crit = ""
        info_miss = ""
        info_dmg = ""
        dmg = round(self.stats['atk'] * (100/(100 + defender.stats['def']*1.5)))
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
            info_crit = ''
            dmg = 0
        return info + info_crit + info_miss + info_dmg

    def check_critical(self):
        '''
        Checks if an attack is critical. If it is, doubles its damage.

        Critical chance comes by the battler's stat: 'critCh'

        Returns:
        True/False : bool
            True if attack is critical, False if it is not
        '''
        if self.stats['critCh'] > random.randint(0, 100):
            return True
        else:
            return False

    def recover_mp(self, amount):
        '''
        Battler recovers certain amount of 'mp' (Mana Points).

        Parameters:
        amount : int
            Amount of mp recovered
        '''
        if self.stats['mp'] + amount > self.stats['maxMp']:
            fully_recover_mp(self)
        else:
            self.stats['mp'] += amount

    def heal(self, amount):
        '''
        Battler recovers certain amount of 'hp' (Health Points).

        Parameters:
        amount : int
            Amount of hp recovered
        '''
        if self.stats['hp'] + amount > self.stats['maxHp']:
            fully_heal(self)
        else:
            self.stats['hp'] += amount

# Returns True if attack misses, False if it doesn't
def check_miss(attacker, defender):
    '''
    Checks if an attack misses or not. Miss chance is determined by the following formula:

    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))

    I tried different formulas and this one ended up being pretty competent. Check if
    it fits you anyway.

    Parameters:
    attacker : Battler
        Battler that performs the attack
    defender : Battler
        Defending battler

    Returns:
    True/False : Bool
        True if the attack missed. False if it doesn't.
    '''
    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))
    if chance > random.randint(0, 100):
        return True
    return False

def check_turns_buffs_and_debuffs(target, deactivate):
    '''
    Checks if buffs and debuffs should still be active (checks its turn count).

    Parameters:
    target : Battler
        Battler whose buffs and debuffs should be checked
    deactivate : bool
        If true, buffs and debuffs deactivate instantly regardless of turn count
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
    Fully heals a target.

    Parameters:
    target : Battler
        Battler to fully heal
    '''
    target.stats['hp'] = target.stats['maxHp']

def fully_recover_mp(target):
    '''
    Fully recovers target's mp.

    Parameters:
    target : Battler
        Battler to fully recover
    '''
    target.stats['mp'] = target.stats['maxMp']

def check_if_loot(player, enemy):
    if random.randint(0, 100) <= enemy.lootChance:
        player.inventory.add_item(inventory.createItem(enemy.possibleLoot))
        return True
    else:
        return False