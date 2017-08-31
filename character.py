import random

def find_dict_by_value(dicts = [{}], key = '', value = None, firstOnly = False):
    '''
    Finds all dictionaries that possess the key:value provided.
    Args:
        dicts (list(dict)): List of dictionaries to search in.
        key (string): The key to search for in the dictionaries.
        value (any): The value associated with the key.
        firstOnly (bool): Return the first dictionary found instead of the list.
    Return:
        result (list(dict)): List of all dictionaries found with the key:value.
        OR
        result (dict): First dictionary found with the key:value.
    '''
    result = (dictionary for dictionary in dicts if dictionary[key] == value)

    if next(result, None) is None:
        result = None
    elif firstOnly:
        result = result.next()

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

def get_modifier(stat = 10):
    '''
    Returns the modifier according to the stat given.
    '''
    return (stat - 10) / 2

def roll(dice = 20, advantage = False, disadvantage = False):
    '''
    Returns a random number between 1 and the specified dice.
    Considers advantage and disadvantage.
    Prints accordingly if fumble or crit happen on a d20.
    Args:
        dice (int): Number to randomize.
    Return:
        result (int): Number rolled.
    '''
    a = random.randint(1, dice)
    b = random.randint(1, dice)

    # Rolling options
    if advantage and not disadvantage:
        print('Rolled {} and {} with advantage'.format(a, b))
        result = max(a, b)
    elif disadvantage and not advantage:
        print('Rolled {} and {} with disadvantage'.format(a, b))
        result = min(a, b)
    else:
        print('Rolled {}'.format(a))
        result = a

    # Crit and fumble monitor if rolling a d20
    if result == 20:
        print('!CRITICAL!')
    elif result == 1 and dice == 20:
        print('!FUMBLE!')

    return result


class Character:
    '''
    Character class containing all information and actions
    related to D&D characters.
    '''

    def __init__(self, buildNew = False, fromFile = None):
        '''
        Constructor function for characters.
        Args:
            buildNew (bool): True to build a new character from scratch
                             when creating a Character object.
            file (string): Path to the character file to build from.
        '''
        if buildNew and fromFile is not None:
            raise Exception('You can\'t build a new character and import one at the same time!')
        # General
        self.level = 0
        self.race = ''
        self.combatClass = ''
        self.alignment = ''
        self.background = ''
        self.hitPointsMax = 0
        self.hitPointsCurrent = 0
        self.hitPointsTemp = 0
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
        # Dict list for weapons and armors
        # Weapon ex: {'name':'Short sword', 'type':'dexterity', 'damage':6, 'damageMod':1, 'hitMod':1}
        # Armor ex:  {'name':'Studded leather', 'baseAC':12, 'bonus':'dexterity'}
        self.weapons = []
        self.armors = []

        if buildNew:
            self._create_character()

    def update_modifiers(self, elements, nameIsType = False):
        '''
        Updates the modifiers of the elements according to this Character's stats.
        Args:
            elements (list(dict)): List of dictionaries to update the modifiers.
            nameIsType (bool): True if the stat type and the name are the same.
        '''

        for e in elements:

            # Set modifier with the appropriate stat
            e['modifier'] = get_modifier(getattr(self, e['name'] if nameIsType else e['type']))
            # Add proficiency if proficient
            if e['proficient']:
                e['modifier'] += get_proficiency(self.level)

    def update_character(self):
        '''
        Updates this whole character from his current stats.
        '''
        self.update_modifiers(self.skills)
        self.update_modifiers(self.savingThrows, True)

    def _create_character(self):
        '''
        BUILT IN
        Creates a character from user input.
        '''
        print('Please enter your character\'s information:')
        for var in vars(self):
            attr = getattr(self, var)
            value = None
            if isinstance(attr, int):
                value = int(raw_input('{}: '.format(var).title()))
            elif isinstance(attr, str):
                value = raw_input('{}: '.format(var).title())
            if value is not None:
                setattr(self, var, value)
        print('Character created. Finalizing...')
        self.update_character()
        print('Done.')
