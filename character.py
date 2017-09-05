import random
import json

def find_dict_by_value(dicts = [{}], key = '', value = None, firstOnly = False):
    '''
    Finds all dictionaries that possess the key:value provided.
    Args:
        dicts (list(dict)): List of dictionaries to search in.
        key (string): The key to search for in the dictionaries.
        value (any): The value associated with the key.
        firstOnly (bool): Return the first dictionary found instead of the list.
    Return:
        result (generator object): Generator object of all dictionaries found with the key:value.
        OR
        result (dict): First dictionary found with the key:value.
    '''
    result = (dictionary for dictionary in dicts if dictionary[key] == value)

    if firstOnly:
        result = next(result, None)

    return result

def get_dices_from_rolls(rolls = '1d4+2d6'):
    '''
    Gets the dice and the multiplier from a string roll expression. (1d4+2d6)
    Args:
        rolls (string): Universal D&D roll format ex: (1d4, 2d8, 3d10).
                        *Can be several dices (4d4+2d8).
    Return:
        result (list(dict)): List of dictionaries containing the value and the
                             multiplier of the roll: {'multiplier':1, 'dice':4}
    '''
    result = []
    dices = rolls.lower().split('+')
    for dice in dices:
        res = dice.split('d')
        result.append({'multiplier':int(res[0]), 'dice':int(res[1])})

    return result

def get_proficiency(level = 1):
    '''
    Returns the proficiency of a character depeding on his level.
    Args:
        level (int): Level of the character.
    Return:
        proficiency (int): Proficiency of the character. (0 if invalid level)

    '''
    prof = 0

    if level < 5:
        prof = 2
    elif level < 9:
        prof = 3
    elif level < 13:
        prof = 4
    elif level < 17:
        prof = 5
    elif level < 21:
        prof = 6

    return prof

def roll(dice = 20, iterator = 1, advantage = False, disadvantage = False):
    '''
    Returns a random number between 1 and the specified dice.
    Considers advantage and disadvantage.
    Prints accordingly if fumble or crit happen on a d20.
    Args:
        dice (int): Number to randomize.
        iterator (int): Number of times to roll the dice.
        advantage (bool): True to roll with advantage, taking the highest of 2 rolls.
        disadvantage (bool): True to roll with disadvantage, taking the lowest of 2 rolls.
    Return:
        result (int): Total of all dice rolled.
    '''
    result = 0

    for i in range(iterator):
        a = random.randint(1, dice)
        b = random.randint(1, dice)
        # Rolling options
        if advantage and not disadvantage:
            print('Rolled {} and {} with advantage'.format(a, b))
            result += max(a, b)
        elif disadvantage and not advantage:
            print('Rolled {} and {} with disadvantage'.format(a, b))
            result += min(a, b)
        else:
            print('Rolled {}'.format(a))
            result += a

        # Crit and fumble monitor if rolling a d20
        if result == 20 and dice == 20:
            print('!CRITICAL!')
        elif result == 1 and dice == 20:
            print('!FUMBLE!')

    return result


class Character:
    '''
    Character class containing all information and actions
    related to D&D characters.
    '''

    def __init__(self, createNew = False, saveFile = None):
        '''
        Constructor function for characters.
        Args:
            createNew (bool): True to build a new character from scratch
                             when creating a Character object.
            saveFile (string): Path to the character file to build from(With ext).
        '''
        if createNew and saveFile is not None:
            raise Exception('You can\'t build a new character and import one at the same time!')

        # General
        self.name = ''
        self.level = 0
        self.race = ''
        self.combatClass = ''
        self.alignment = ''
        self.background = ''
        self.hitPointsMax = 0
        self.hitPointsCurrent = 0
        self.hitPointsTemp = 0
        self.hitDice = 0
        self.armorClass = 0
        self.proficiency = 0
        self.initiative = 0
        self.speed = 0

        # Stats
        self.strenght = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.passivePerception = 0

        # Money
        self.purse = {'copper':0, 'silver':0, 'electrum':0, 'gold':0, 'platinum':0}

        # Spells
        # Spell save dc = 8 + prof + class modifier
        # Spell attack modifier = Prof + class modifier
        self.spellDC = 0
        self.spellAttack = 0
        # Temp
        self.classSpellModifier = ''
        self.classSpellRessource = {'name':'', 'maximum':0, 'current':0}

        # Saving throws
        self.savingThrows = [{'name':'strenght', 'modifier':0, 'proficient':False},
                             {'name':'dexterity', 'modifier':0, 'proficient':False},
                             {'name':'constitution', 'modifier':0, 'proficient':False},
                             {'name':'intelligence', 'modifier':0, 'proficient':False},
                             {'name':'wisdom', 'modifier':0, 'proficient':False},
                             {'name':'charisma', 'modifier':0, 'proficient':False}]

        # Skills
        self.skills = [{'name':'acrobatics', 'type':'dexterity', 'modifier':0, 'proficient':False},
                       {'name':'animalHandling', 'type':'wisdom', 'modifier':0, 'proficient':False},
                       {'name':'arcana', 'type':'intelligence', 'modifier':0, 'proficient':False},
                       {'name':'athletics', 'type':'strenght', 'modifier':0, 'proficient':False},
                       {'name':'deception', 'type':'charisma', 'modifier':0, 'proficient':False},
                       {'name':'history', 'type':'intelligence', 'modifier':0, 'proficient':False},
                       {'name':'insight', 'type':'wisdom', 'modifier':0, 'proficient':False},
                       {'name':'intimidation', 'type':'charisma', 'modifier':0, 'proficient':False},
                       {'name':'investigation', 'type':'intelligence', 'modifier':0, 'proficient':False},
                       {'name':'medecine', 'type':'wisdom', 'modifier':0, 'proficient':False},
                       {'name':'nature', 'type':'intelligence', 'modifier':0, 'proficient':False},
                       {'name':'perception', 'type':'wisdom', 'modifier':0, 'proficient':False},
                       {'name':'performance', 'type':'charisma', 'modifier':0, 'proficient':False},
                       {'name':'persuassion', 'type':'charisma', 'modifier':0, 'proficient':False},
                       {'name':'religion', 'type':'intelligence', 'modifier':0, 'proficient':False},
                       {'name':'sleightOfHand', 'type':'dexterity', 'modifier':0, 'proficient':False},
                       {'name':'stealth', 'type':'dexterity', 'modifier':0, 'proficient':False},
                       {'name':'survival', 'type':'wisdom', 'modifier':0, 'proficient':False}]

        # Equipment
        # Dict list of equipment from the config file. Custom equipment can
        # be added there. They need to respect the basic keys though.
        # Weapon ex: {'name':'Short sword', 'type':'dexterity', 'damage':1d6, 'damageMod':1, 'hitMod':1, 'proc':1d6}
        # Armor ex:  {'name':'Studded leather', 'baseAC':12, 'bonus':'dexterity', 'modifier':2, 'maxBonus':3}
        self.weapons = []
        self.armors = []
        self.tools = []
        self.misc = []
        self.scrolls = []
        self.potions = []

        if createNew:
            self._create()

        if saveFile is not None:
            self.load(saveFile)

    def get_modifier(self, stat):
        '''
        Returns the modifier according to the int given.
        If stat is a string, takes this character's stat value instead.
        Args:
            stat (int or string): Stat to get the modifier from.
        Return:
            modifier (int): Modifier of the stat.
        '''
        return (stat - 10) / 2 if isinstance(stat, int) else (getattr(self, stat) - 10) / 2

    def update_modifiers(self, elements, nameIsType = False):
        '''
        Updates the modifiers of the elements according to this Character's stats.
        (elements) has to have those specific keys:
            modifier:(int)
            type:(str)
            proficient:(bool)
            ***name:(str) if [type] == [name]

        Args:
            elements (list(dict)): List of dictionaries to update the modifiers.
            nameIsType (bool): True if the stat type and the name are the same.
        '''

        for e in elements:

            # Set modifier with the appropriate stat
            e['modifier'] = self.get_modifier(getattr(self, e['name'] if nameIsType else e['type']))
            # Add proficiency if proficient
            if e['proficient']:
                e['modifier'] += get_proficiency(self.level)

    def update(self):
        '''
        Updates this whole character from his current stats.
        TODO:
            Take equipement into consideration
            Take active spells into consideration
        '''
        self.proficiency = get_proficiency(self.level)
        self.update_modifiers(self.skills)
        self.update_modifiers(self.savingThrows, True)
        self.spellAttack = self.proficiency + self.get_modifier(getattr(self, self.classSpellModifier))
        self.spellDC = 8 + self.spellAttack
        self.initiative = self.get_modifier('dexterity')
        self.passivePerception = 10 + self.get_modifier('wisdom')
        self.passivePerception += self.proficiency if find_dict_by_value(self.skills, 'name', 'perception', True)['proficient'] else 0
        if not self.armors:
            self.armorClass = 10 + self.get_modifier('dexterity')
        self.hitPointsCurrent = self.hitPointsTemp = self.hitPointsMax

    def attack(self, weapon = {}, advantage = False, disadvantage = False, additionalRolls = None):
        '''
        Attack with the provided weapon using this character stats.
        Weapon ex: {'name':'short sword', 'type':'dexterity', 'damage':'1d6', 'damageMod':1, 'hitMod':1, 'proc':'1d6', 'proficient': False}
        TODO:
            Need to fully implement the get_dices_from_rolls with standard damage and proc.
        Args:
            weapon (dict): Weapon to attack with. Attacks with fist if no weapon is provided.
            advantage (bool): True to roll with advantage, taking the highest of 2 rolls.
            disadvantage (bool): True to roll with disadvantage, taking the lowest of 2 rolls.
            additionalRolls (string): Rolls to add custom damage to the attack.
        '''
        print('Attacking with {}.'.format(weapon['name']))
        # Getting character modifier for this weapon
        statModifier = self.get_modifier(weapon['type'])
        # Getting dices to calculate weapon damage
        damageDice = get_dices_from_rolls(weapon['damage'])[0]
        print('Rolling hit.')
        # Calculating the total hit dice depeding of the character and the proficiency
        hit = roll(advantage = advantage, disadvantage = disadvantage)
        totalHit = hit + statModifier + weapon['hitMod']
        totalHit += self.proficiency if weapon['proficient'] else 0
        print('Hit for a total of {}!'.format(totalHit))
        print('Rolling damage.')
        # Calculating total damage
        damage = roll(dice = damageDice['dice'], iterator = damageDice['multiplier'])
        damage += damage if hit == 20 else 0
        totalDamage = damage + statModifier + weapon['damageMod']
        print('Weapon damage: {}'.format(totalDamage))
        # Calculating proc or bonus damage if the weapon has one
        if weapon['proc'] is not 0:
            print('Rolling weapon bonus damage/proc.')
            procDice = get_dices_from_rolls(weapon['proc'])[0]
            proc = roll(dice = procDice['dice'], iterator = procDice['multiplier'])
            print('Weapon proc\'d for an additonal {} damage.'.format(proc))
            totalDamage += proc

        if additionalRolls is not None:
            print('Adding custom rolls to the attack: {}'.format(additionalRolls))
            dices = get_dices_from_rolls(additionalRolls)
            for dice in dices:
                damage = roll(dice = dice['dice'], iterator = dice['multiplier'])
                print('Additional damage roll: {}'.format(damage))
                totalDamage += damage
        print('Attack recap: {} hit for {} with a grand total of {} damage.'.format(weapon['name'], totalHit, totalDamage))

    def save(self, saveFile = 'default.txt'):
        '''
        Saves this character in the JSON format.
        '''
        with open(saveFile, 'w+') as sf:
            json.dump(self.__dict__, sf, sort_keys = True, indent = 4)

    def load(self, saveFile = 'default.txt'):
        '''
        Loads and replaces this character by the specified JSON format file.
        '''
        with open(saveFile, 'r+') as sf:
            self.__dict__ = json.load(sf)


    def _create(self, fromScratch = False):
        '''
        PRIVATE: Should be only used once, in the __init__!
        Creates a character from user input.
        Args:
            fromScratch (bool): Create your character from scratch, meaning that
                                choosing the race, class and background will
                                apply the bonuses to your stats automatically.
                                TODO - WIP
        '''
        # Requesting basic fields to the user
        requiered = ['name',
                     'combatClass',
                     'race',
                     'alignment',
                     'background',
                     'level',
                     'hitPointsMax',
                     'speed',
                     'strenght',
                     'dexterity',
                     'constitution',
                     'intelligence',
                     'wisdom',
                     'charisma',
                     'classSpellModifier']

        print('Please enter your character\'s information:')
        # Asking for requiered attributes
        for field in requiered:
            # Get actual value
            attr = getattr(self, field)
            value = None
            # Request user input, converts to int if needed.
            if isinstance(attr, int):
                value = int(raw_input('{}: '.format(field).title()))
            elif isinstance(attr, str):
                value = raw_input('{}: '.format(field).title())
            if value is not None:
                # Set value only if it has changed.
                setattr(self, field, value)
        # Asking for proficiencies
        print('Please select your proficiencies, use yes or y if the case, else no or n.')
        for st in self.savingThrows:
            proficient = raw_input('Are you proficient in {} saving throws?'.format(st['name']))
            st['proficient'] = True if proficient.lower().startswith('y') else False
        for skill in self.skills:
            proficient = raw_input('Are you proficient in {}?'.format(skill['name']))
            skill['proficient'] = True if proficient.lower().startswith('y') else False
        # Setting purse
        print('Please enter your glorious wealth.')
        for coin, amount in self.purse.iteritems():
            value = raw_input('{}: '.format(coin).title())
            self.purse[coin] = int(value) if value != '' else 0
        # Setting vairables
        print('Character created. Finalizing...')
        self.update()
        print('Done.')

    def _print(self):
        '''
        PRIVATE: Used for debug.
        Prints all this object's attributes with their value in STDOUT.
        '''
        print('Printing character...')
        for var in vars(self):
            print('{}: {}'.format(var , vars(self).get(var)))
