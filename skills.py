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

    def __init__(self, name, description, cost) -> None:
        self.name = name
        self.description = description
        self.cost = cost
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

    def __init__(self, name, description, power, cost) -> None:
        super().__init__(name, description, cost)
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

class Combo(Skill):
    '''
    Combos consume cp (Combo Points), which counter is by default set to 0 when a battle
    starts and increment as the Battler performs normal attacks. They can also increment
    by using certain Skills. They usually have special effects and integrates normal
    attacks within them. Inherits from Skill.
    '''

    def __init__(self, name, description, cost) -> None:
        super().__init__(name, description, cost)

    def check_cp(self, caster):
        '''
        Checks if caster has enough CP to perform the combo.

        Parameters:
        caster : Battler
            Performer of the combo.

        Returns:
        True/False : bool
            True if combo was performed succesfully. False if it didn't.
        '''
        if caster.comboPoints < self.cost:
            #print('Not enough Combo Points!')
            return False
        else:
            #print(f'{caster.name} uses {self.name}!')
            caster.comboPoints -= self.cost
            return True

##### SPELLS #####

class DamageSpell(Spell):
    '''
    Standard damaging Spell class. Inherits from Spell.
    '''
    def __init__(self, name, description, power, mpCost) -> None:
        super().__init__(name, description, power, mpCost)
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

    def __init__(self, name, description, power, mpCost) -> None:
        super().__init__(name, description, power, mpCost)
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
        spell = DamageSpell(spell_json['name'], spell_json['description'], spell_json['power'], spell_json['cost'])
    elif skill_type == 'HealingSpell':
        spell = HealingSpell(spell_json['name'], spell_json['description'], spell_json['power'], spell_json['cost'])
    return spell

# COMBOS
    # Swords
class SwordSlashCombo(Combo):
    '''
    Slashes with your sword X times
    '''
    def __init__(self, name, description, cost, hits) -> None:
        super().__init__(name, description, cost)
        self.hits = hits
        self.skillType = 'SwordSlashCombo'

    def effect(self, caster, target):
        '''
        Deals damage based on combo to target.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_cp(caster):
            cast_info = f"{caster.name} performs {self.name}!\n"
            player_txt = ""
            for i in range(self.hits):
                player_txt += caster.normal_attack(target)
            return cast_info + player_txt

        return f"You do not have enough Combo Points to perform {self.name}, {caster.name}\n"

    # Daggers
class CriticalStrikeCombo(Combo):
    def __init__(self, name, description, cost) -> None:
        super().__init__(name, description, cost)
        self.skillType = 'CriticalStrikeCombo'

    def effect(self, caster, target):
        '''
        Deals damage based on combo to target.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_cp(caster):
            cast_info = f"{caster.name} performs {self.name}!\n"
            player_txt = ""
            original_crit = caster.stats['critCh']
            original_speed = caster.stats['speed']

            caster.stats['critCh'] = 100
            caster.stats['speed'] = original_speed - original_speed / 3

            player_txt += caster.normal_attack(target)
            caster.stats['critCh'] = original_crit
            caster.stats['speed'] = original_speed

            return cast_info + player_txt

        return f"You do not have enough Combo Points to perform {self.name}, {caster.name}\n"

    # Bows
class PerfectAimCombo(Combo):
    def __init__(self, name, description, cost) -> None:
        super().__init__(name, description, cost)
        self.skillType = 'PerfectAimCombo'

    def effect(self, caster, target):
        '''
        Deals damage based on combo to target.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_cp(caster):
            cast_info = f"{caster.name} performs {self.name}!\n"
            player_txt = ""

            original_speed = target.stats['speed']

            target.stats['speed'] = 0

            player_txt += caster.normal_attack(target)

            target.stats['speed'] = original_speed

            return cast_info + player_txt

        return f"You do not have enough Combo Points to perform {self.name}, {caster.name}\n"

    # Axes & Hammers
class DestroyerStrikeCombo(Combo):
    def __init__(self, name, description, cost) -> None:
        super().__init__(name, description, cost)
        self.skillType = 'DestroyerStrikeCombo'

    def effect(self, caster, target):
        '''
        Deals damage based on combo to target.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_cp(caster):
            cast_info = f"{caster.name} performs {self.name}!\n"
            player_txt = ""

            original_def = target.stats['def']

            target.stats['def'] = original_def * 0.5

            player_txt += caster.normal_attack(target)
            target.stats['def'] = original_def

            return cast_info + player_txt

        return f"You do not have enough Combo Points to perform {self.name}, {caster.name}\n"

    # Staffs
class RecoverCombo(Combo):
    def __init__(self, name, description, cost, stat, amountToRecover) -> None:
        super().__init__(name, description, cost)
        self.stat = stat
        self.amountToRecover = amountToRecover
        self.skillType = 'RecoverCombo'

    def effect(self, caster, target):
        '''
        Deals damage based on combo to target.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_cp(caster):
            cast_info = f"{caster.name} performs {self.name}!\n"
            player_txt = f"{caster.name} recovers {self.amountToRecover} {self.stat}\n"

            if self.stat == 'hp':
                caster.heal(self.amountToRecover)
            else:
                caster.recover_mp(self.amountToRecover)

            return cast_info + player_txt
        return f"You do not have enough Combo Points to perform {self.name}, {caster.name}\n"


def createCombo(combo_json):
    skill_type = combo_json['skillType']
    if skill_type == 'SwordSlashCombo':
        combo = SwordSlashCombo(combo_json['name'], combo_json['description'], combo_json['cost'], combo_json['hits'])
    elif skill_type == 'CriticalStrikeCombo':
        combo = CriticalStrikeCombo(combo_json['name'], combo_json['description'], combo_json['cost'])
    elif skill_type == 'PerfectAimCombo':
        combo = PerfectAimCombo(combo_json['name'], combo_json['description'], combo_json['cost'])
    elif skill_type == 'DestroyerStrikeCombo':
        combo = DestroyerStrikeCombo(combo_json['name'], combo_json['description'], combo_json['cost'])
    elif skill_type == 'RecoverCombo':
        combo = RecoverCombo(combo_json['name'], combo_json['description'], combo_json['cost'], combo_json['stat'], combo_json['amountToRecover'])
    return combo

##### SPELL & COMBO INSTANCES #####

# Spells
    # Damaging
spellSmallFireball = DamageSpell('Small Fireball', 'Small fire explosion thrown from the tip of your fingers', 10, 4)
spellFireball = DamageSpell('Fireball', 'A medium-sized fireball to decimate your opponents', 18, 6)

    # Healing
spellSmallBlessing = HealingSpell('Small Blessing', 'Recovers a small amount of HP', 10, 5)

# Combos
    # Damaging
comboSwordSlash = SwordSlashCombo('Sword Slash', 'Slash twice with your sword in a single turn', 3, 2)
comboCriticalStrike = CriticalStrikeCombo('Critical Strike', 'Performs a critical hit, but it is not too accurate', 2)
comboPerfectAim = PerfectAimCombo('Perfect Aim', 'Attacks with 100% accuracy', 2)
comboDestroyerStrike = DestroyerStrikeCombo('Destroyer Strike', 'Strike your enemy ignoring 50% of its physical defense', 2)
comboQuickMeditation = RecoverCombo('Quick Meditation', 'Recovers a small amount of MP', 2, 'mp', 8)

combo_learn = {"Swords" : {2 : comboSwordSlash}, "Axes & Hammers" : {2 : comboDestroyerStrike}, "Daggers" : {2 : comboCriticalStrike}, "Bows" : {2 : comboPerfectAim}, "Staffs & Scythes" : {2 : comboQuickMeditation}}