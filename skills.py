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
        self.skillType = ""

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
        self.skillType = 'DamageSpell'

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
            dmg = round(self.power * caster.stats['matk'] * 0.7 / target.stats['mdef'] + self.power / 2)
            return cast_info + target.take_dmg(dmg)
        return f"You do not have enough MP to cast {self.name}, {caster.name}\n"

class HealingSpell(Spell):
    '''
    Standard healing Spell class. Inherits from Spell.
    '''

    def __init__(self, name, description, power, mpCost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)
        self.skillType = 'HealingSpell'

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
            heal_power = round((self.power + caster.stats['matk'] * 0.5)/2 + self.power/4)
            return cast_info + target.heal(heal_power)

        return f"You do not have enough MP to cast {self.name}, {caster.name}\n"

def createSpell(spell_json):
    skill_type = spell_json['skillType']
    if skill_type == 'DamageSpell':
        spell = DamageSpell(spell_json['name'], spell_json['description'], spell_json['power'], spell_json['cost'], spell_json['isTargeted'], spell_json['defaultTarget'])
    elif skill_type == 'HealingSpell':
        spell = HealingSpell(spell_json['name'], spell_json['description'], spell_json['power'], spell_json['cost'], spell_json['isTargeted'], spell_json['defaultTarget'])
    return spell

##### SPELL & COMBO INSTANCES #####

# Damaging
spellSmallFireball = DamageSpell('Small Fireball', '', 10, 4, True, None)
spellFireball = DamageSpell('Fireball', '', 18, 6, True, None)

# Healing
spellSmallBlessing = HealingSpell('Small Blessing', '', 10, 5, True, None)