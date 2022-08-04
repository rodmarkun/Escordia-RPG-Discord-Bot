import random
import math

'''
Parent class for all instances that can enter in combat.
A Battler will always be either an Enemy, a Player's ally or the Player himself
'''
class Battler():
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
        print(f'{self.name} takes {dmg} damage!')
        # Defender dies
        if self.stats['hp'] <= 0:
            print(f'{self.name} has been slain.')
            self.alive = False

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
        print(f'{self.name} attacks!')
        dmg = round(self.stats['atk'] * (100/(100 + defender.stats['def']*1.5)))
        # Check for critical attack
        dmg = self.check_critical(dmg)
        # Check for missed attack
        if not check_miss(self, defender):
            defender.take_dmg(dmg)
        else:
            dmg = 0
        return dmg

    def check_critical(self, dmg):
        '''
        Checks if an attack is critical. If it is, doubles its damage.

        Critical chance comes by the battler's stat: 'critCh'

        Parameters:
        dmg : int
            Base damage dealt

        Returns:
        dmg : int
            Damage dealt (after checking and operating if critical)
        '''
        if self.stats['critCh'] > random.randint(0, 100):
            print('Critical blow!')
            return dmg * 2
        else:
            return dmg

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
        print(f'{self.name} recovers {amount} mp!')

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
        print(f'{self.name} heals {amount} hp!')

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
        print(f'{attacker.name}\'s attack missed!')
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

# Checks if a battler is dead and removes it from the appropiate lists
def check_if_dead(allies, enemies, battlers):
    '''
    Checks if current battlers are dead and if they are, removes them from
    the corresponding lists.

    Parameters:
    allies : List
        List of ally Battlers
    enemies : List
        List of enemy Battlers
    battlers : List
        List of all battlers
    '''
    # TODO: This can probably be done in an easier way, but iterating
    # while deleting objects leads to weird stuff happening.
    dead_bodies = []
    for ally in allies:
        if ally.alive == False:
            dead_bodies.append(ally)
    for target in enemies:
        if target.alive == False:
            dead_bodies.append(target)
    for dead in dead_bodies:
        if dead in battlers:
            battlers.remove(dead)
        if dead in enemies:
            enemies.remove(dead)
        elif dead in allies:
            allies.remove(dead)

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