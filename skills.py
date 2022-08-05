class Skill():
    '''
    Skill is the parent class for Spells and Combos.

    Attributes:
    name : str
        Name of the skill.
    description : str
        Skill's description.
    cost : int
        Cost of MP or CP.
    isTargeted : bool
        True if a target must be chosen, False if there is a default target.
    defaultTarget : str
        Default target if spell is not targeted.
    '''

    def __init__(self, name, description, cost, isTargeted, defaultTarget) -> None:
        self.name = name
        self.description = description
        self.cost = cost
        self.isTargeted = isTargeted
        self.defaultTarget = defaultTarget

    def check_already_has_buff(self, target):
        '''
        Checks if target Battler already has a buff from this skill.
        Skill's name bust be equal to buff's.

        Parameters:
        target : Battler
            Target to check if already has this buff.

        Returns:
        True/False : bool
            True if Battler already had buff. False if it didn't.
        '''
        for bd in target.buffsAndDebuffs:
            if bd.name == self.name:
                print(f'{target.name} has their {self.name}\'s duration restarted')
                bd.restart()
                return True
        return False


class Spell(Skill):
    '''
    Spells consume mp (Magic Points), which are restored by leveling up, using items,
    events... They also increment when upgrading the WIS (Wisdom) aptitude or equipping
    certain items. They use matk (Magic Attack) and their own power to calculate the
    damage done. Inherits from Skill.

    Attributes:
    power : int
        Power this spell has.
    '''

    def __init__(self, name, description, power, cost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.power = power

    def check_mp(self, caster):
        '''
        Checks if caster has enough MP to cast the spell.

        Parameters:
        caster : Battler
            Caster of the spell.

        Returns:
        True/False : bool
            True if spell was casted succesfully. False if it didn't.
        '''
        if caster.stats['mp'] < self.cost:
            #print('Not enough MP!')
            return False
        else:
            #print(f'{caster.name} casts {self.name}!')
            caster.stats['mp'] -= self.cost
            return True

    def effect(self, caster, target):
        pass

##### SPELLS #####

class DamageSpell(Spell):
    '''
    Standard damaging Spell class. Inherits from Spell.
    '''
    def __init__(self, name, description, power, mpCost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)

    def effect(self, caster, target):
        '''
        Deals damage based on spell's power to target.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_mp(caster):
            cast_info = f"{caster.name} casts {self.name}!\n"
            if self.isTargeted:
                dmg = self.power + (caster.stats['matk'] - target.stats['mdef'])
                return cast_info + target.take_dmg(dmg)
            else:
                if self.defaultTarget == 'all_enemies':
                    for enemy in target:
                        dmg = self.power + (caster.stats['matk'] - enemy.stats['mdef'])
                        enemy.take_dmg(dmg)
        return f"You do not have enough MP to cast {self.name}, {caster.name}"

def createSpell(spell_json):
    spell = DamageSpell(spell_json['name'], spell_json['description'], spell_json['power'], spell_json['cost'], spell_json['isTargeted'], spell_json['defaultTarget'])
    return spell

##### SPELL & COMBO INSTANCES #####

spellFireball = DamageSpell('Fireball', '', 15, 3, True, None)