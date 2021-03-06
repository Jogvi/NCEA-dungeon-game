import pickle as p
import random as r
import webbrowser as w
import time as t

yes_inputs = ['yes', 'y', 'yea', 'yeah', 'yep', 'yesaroo']
no_inputs = ['no', 'n', 'nope', 'back', 'b', 'cancel', 'c']
delve_inputs = ['yes', 'y', 'delve', 'd', 'deeper', 'deep']
home_inputs = ['h', 'home', 'back', 'b']
save_inputs = ['s', 'save']
load_inputs = ['l', 'load']
equipable = [1, 2, 3, 4, 5]
potion_pouch = []

item_bought = ''

slot_dict = {
    1: 'Save_Files\\Save1.pkl',
    2: 'Save_Files\\Save2.pkl',
    3: 'Save_Files\\Save3.pkl'
}
stock_dict = {
    5: 'Stages\\Shop\\Trinkets_stocks.txt',
    6: 'Stages\\Shop\\Potions_stocks.txt',
    7: 'Stages\\Shop\\Amulets_stocks.txt',
    8: 'Stages\\Shop\\Enchantments_stocks.txt',
    9: 'Stages\\Shop\\Bows_&_arrows_stocks.txt',
}

# w.open('https://www.youtube.com/watch?v=xvFZjo5PgG0')

item_types = {
    'Shortbow': 6,
    'Bow': 6,
    'Longbow': 6,
    '10 arrows': 7,
    '50 arrows': 7,
    '100 arrows': 7,
    '5 Fire Arrows': 7,
    'Small quiver': 8,
    'Medium quiver': 8,
    'Large quiver': 8,
}


def save_game():
    try:
        slot = int(input('what save slot would you like to use?'))
    except ValueError:
        print('Sorry, that is not a valid slot...')
        save_game()
    save_file = 'Save_Files\\Save1.pkl'
    if slot == 1:
        save_file = 'Save_Files\\Save1.pkl'
    elif slot == 2:
        save_file = 'Save_Files\\Save2.pkl'
    elif slot == 3:
        save_file = 'Save_Files\\Save3.pkl'
    p.dump(player, open(save_file, "wb"))
    print(f'you have successfully saved {player.name} in slot {slot}!')


def save(obj, file):
    p.dump(obj, open(file, 'wb'))


def load(file):
    with open(file, 'rb') as data:
        obj = p.load(data)
    return obj


def load_game():
    global player
    slot = slot_dict[int(input('What slot would you like to load?'))]
    with open(slot, 'rb') as data:
        player = p.load(data)
    return player


def home():
    print('end of the game')
    game_over()


def header():
    print('header')
    # do later


def level_up():
    print('Level UP!')
    try:
        action = int(input("Would you like to raise your max health(0) or your strength(1)?"))
        if action > 1:
            raise ValueError
    except ValueError:
        print("Oops... Let's try again")
        level_up()
    if action == 0:
        print(f'Your max health has raised from {player.mhealth} to {int(player.mhealth * 1.1)}')
        player.mhealth = int(player.mhealth * 1.1)
    elif action == 1:
        print(f'Your strength has raised from {round(player.damage, 4)} to {round(player.damage * 1.1, 4)}')
        player.damage *= 1.1
    player.health = player.mhealth
    print(f"You feel refreshed... You've healed beck to your max, {player.mhealth} health points")
    player.level += 1
    menu()

def menu_init():
    if player.invincibility > 0:
        player.invincibility -= 1
    if player.xp >= player.level * 50:
        level_up()
    player.temp_damage = player.damage * player.equipped_weapon.damage
    player.total_armour_class = player.headwear.armour + player.body_armour.armour \
                                + player.pants.armour + player.footwear.armour
    

def menu():
    global player
    menu_init()
    print(f'You have {player.health} health points left. Would you like to delve '
                   'deeper in the dungeon, or go home? You can also choose to save by '
                   f'typing "{save_inputs[0]}" or "{save_inputs[1]}"'
                   f'and load with "{load_inputs[0]}" or "{load_inputs[1]}" \n')
    t.sleep(1)
    action = input()

    if action in delve_inputs:
        delve()
    elif action in home_inputs:
        home()
    elif action in save_inputs:
        save_game()
    elif action in load_inputs:
        player = load_game()
        print(f'You have loaded {player.name}')
        menu()
    else:
        menu()


def delve():
    stage = r.randint(0, 100)
    if stage <= 0:
        while True:
            monster = r.choice(monsters)
            if monster.level <= player.level:
                break
        if monster.level == 1:
            print(f'A wild {monster.name} appears!')
        elif monster.level == 2:
            print(f'A scary {monster.name} appears!')
        elif monster.level == 3:
            print(f'A menacing {monster.name} appears!')
        elif monster.level == 4:
            print(f'A terrifying {monster.name} appears!')
        fight(monster)
    elif stage <= 95:
        shop()
    elif stage <= 99:
        healer()
    else:
        print('You enter an empty room...')
        menu()


def ask_potion(monster):
    useable_potions = []
    action = input('Would you like to use a potion?')
    if action in yes_inputs:
        for i in player.backpack:
            if i.level == 0:
                useable_potions.append(i)
        if len(useable_potions) > 0:
            for a in range(len(useable_potions)):
                print('1:', useable_potions[a].name)
                try:
                    action = int(input('What potion would you like to use?'))-1
                    if action >= len(useable_potions):
                        raise ValueError
                except ValueError:
                    print("Oops")
                    ask_potion(monster)
                useable_potions[action].use(monster)
        else:
            print('Oops, you do not have any potions')


def fight(monster):
    damage = int(monster.damage * (r.randint(1, 100) / 100 + 1))
    player_damage = int((player.temp_damage * r.randint(1, 150) / 100) + 1)
    if player.invincibility <= 0 and damage > 0:
        player.health -= damage
        print(f'The {monster.name} deals you {damage - player.total_armour_class} damage')
    elif damage <= 0:
        print(f'The {monster.name} weakly throws his arms, but it is not enough to harm you')
    monster.health -= player_damage
    if player.health <= 0:
        print(f'The {monster.name} kills you. This is the end of the tale of {player.name}')
        game_over()
    else:
        if monster.health > 0:
            ask_potion(monster)

            print(f'You retaliate, causing it {player_damage} damage! It now has {monster.health} hp left!')
            print(f'You have {player.health} hp left!')
            input('Press [Enter] to continue')
            fight(monster)
        else:
            print(f'The {monster.name} dies after you deal it {player_damage} damage')
            player.score += monster.level
            monster.health = monster.max_health
            player.money += monster.money
            player.xp += monster.xp_given
            print(f'The {monster.name} dropped {monster.money} Ducats and {monster.xp_given} xp')
            if player.xp < player.level * 50:
                print(f'You now have {player.xp} xp, and need {player.level * 50} to level up.')
            menu()


def equip_item(item):
    if item.type == 0:
        player.equipped_weapon = item
        menu()
    elif item.type == 1:
        player.headwear = item
        menu()
    elif item.type == 2:
        player.body_armour = item
        menu()
    elif item.type == 3:
        player.pants = item
        menu()
    elif item.type == 4:
        player.footwear = item
        menu()
    elif item.type == 5:
        action = int(input(f'Would you like to equip your {item.name} as a '
                           'right wrist bracelet(1), a left wrist bracelet(2) or'
                           'a necklace(3)?'))
        if action == 1:
            player.bracelet1 = item
            print(f"Your new right bracelet is a {player.bracelet1.name}")
        elif action == 2:
            player.bracelet2 = item
            print(f"Your new left bracelet is a {player.bracelet2.name}")
        elif action == 3:
            player.necklace = item
            print(f"Your new necklace is a {player.necklace.name}")
        menu()


def bank():
    if input('would you like to use our services?') in yes_inputs:
        action = int(input('What would you like to do? (1:Deposit; 2:Withdrawal, 3:Borrow money'))
        if action == 1:
            deposit_amount = int(input('How much would you like to deposit?'))
            if deposit_amount <= player.money:
                if input(f'You are about to deposit {deposit_amount} ducats. Are you sure?') in yes_inputs:
                    player.money -= deposit_amount
                    player.bank_money += deposit_amount
                else:
                    bank()
            else:
                print('I would love to relieve you of **that** amount, but you do not have enough money...')
                input('[Enter] to continue')
                bank()
        elif action == 2:
            if player.bank_money == 0:
                print("You don't even have money here! Please deposit before you start withdrawing...")
            withdrawal_amount = int(input("how much would you like to withdraw"))
            if withdrawal_amount <= player.bank_money:
                player.bank_money -= player.bank_money
                print(f'You withdrew {withdrawal_amount} ducats')
        else:
            if player.bank_money > 0:
                print(f'Sorry, your bank account only has {player.bank_money} ducats')


def remove_character(item, remove):
    out = ""
    for i in range(0, len(item)):
        if item[i] not in remove:
            out = out + item[i]
        else:
            out = out + " "
    out = out.title()
    return out


def shop():
    with open('Stages\\Shop\\Shops.txt', 'r') as f:
        content = f.readlines()
    shop_id = r.randint(0,3)
    shopkeeper_id = r.randint(4,len(content))
    shop_name = content[shop_id].strip()
    shopkeeper = content[shopkeeper_id].strip()
    with open('Stages\\Shop\\Shop_Descriptions.txt', 'r') as f:
        content = f.readlines()
        shop_description = content[shop_id]
    print(f"welcome to {shopkeeper}'s {shop_name}. I am {shopkeeper}.")
    t.sleep(1)
    print(shop_description)
    input('Press [Enter] to continue')
    # if shop is inferior to 3 it is a service
    print('this is what we have on sale')
    shop_stock = stock_dict[shop_id]
    with open(shop_stock, 'r') as f:
        content = f.readlines()
    items_on_sale = []
    loop = 0
    while loop < 3:
        item = content[r.randint(0, len(content)-1)].strip()
        if eval(item).level <= player.level:
            items_on_sale.append(item)
            print(f'{loop + 1}:{eval(item).name} : {eval(item).price}')
            loop += 1
            t.sleep(0.3)
    action = input('Would you like to buy something?You currently have '
                       f'{player.money} Ducats \n')
    if action in yes_inputs:
        t.sleep(0.2)
        action = int(input('What would you like to buy? (1,2 or 3)\n'))
        global item_bought
        item = items_on_sale[action - 1]
        item = eval(item)
        if item.price <= player.money:
            player.money -= item.price
            if item.equippable:
                action = input(f'Do you want to equip your new {item.name}? \n')
                if action in yes_inputs:
                    t.sleep(0.5)
                    equip_item(item)
                elif action in no_inputs:
                    player.backpack.append(item)
                else:
                    print("I think you've misspelled your input")
                
        else:
            print('sorry, you dont have enough money...')
            t.sleep(2)
            shop()
    else:
        print('See you soon!')
    elif shop_id == 1:
        bank()
    menu()


def healer():
    print('healer')
    # do later
    menu()


def game_over():
    action = input('would you like to save your score and name? \n')
    if action in yes_inputs:
        with open('Save_Files\\Saved_Scores.txt', 'r') as f:
            content = f.readlines()
        with open('Save_Files\\Saved_Scores.txt', 'w') as f:
            f.write(' '.join(content))
            f.write('\n')
            f.write(str(player.score).strip())
            f.write('\n')
            f.write(player.name.strip())


class Enemies:
    def __init__(self, name, damage, max_health, money, xp, level):
        self.name = name
        self.damage = damage
        self.health = max_health
        self.max_health = max_health
        self.level = level
        self.money = money
        self.xp_given = xp


null_monster = Enemies('', 0, 0, 0, 0, 99)
goblin = Enemies('goblin', 5, 200, 5, 10, 1)
bat = Enemies('bat', 1, 1, 100, 1, 1)
skeleton = Enemies('skeleton', 8, 100, 10, 5, 1)
ogre = Enemies('Ogre', 30, 500, 20, 15, 2)

monsters = [goblin, skeleton, bat]


class Armour:
    def __init__(self, name, armour, solidity, level, item_type, price):
        self.name = name
        self.armour = armour
        self.solidity = solidity
        self.level = level
        self.type = item_type
        self.price = price
        self.equippable = True


no_armour = Armour("nothing", 0, 0, 0, 0, 0)
sweaty_underpants = Armour("Sweaty Underpants", 1, 69, 0, 3, 1)
bucket = Armour("Bucket", 3, 50, 0, 1, 35)
leather_breastplate = Armour("Leather Breastplate", 5, 100, 1, 2, 50)
leather_pants = Armour("Leather Pants", 5, 90, 1, 3, 40)
leather_boots = Armour("Leather Boots", 3, 80, 1, 4, 35)
bronze_helm = Armour("Bronze Helmet", 7, 100, 1, 1, 100)
bronze_breastplate = Armour('Bronze Breastplate', 10, 100, 1, 2, 150)
bronze_pants = Armour('Bronze Pants', 8, 100, 1, 3, 125)
bronze_boots = Armour('Bronze Boots', 8, 90, 1, 4, 115)
silver_helm = Armour('Silver Helmet', 13, 125, 2, 1, 200)
silver_breastplate = Armour('Silver Breastplate', 15, 100, 2, 2, 215)
silver_pants = Armour('Silver Pants', 14, 115, 2, 3, 210)
silver_boots = Armour('Silver Boots', 12, 150, 2, 4, 195)
gold_helm = Armour('Gold Helmet', 17, 90, 3, 1, 300)
gold_breastplate = Armour('Gold Breastplate', 20, 100, 3, 2, 350)
gold_pants = Armour('Gold Pants', 18, 100, 3, 3, 325)
gold_boots = Armour('Gold Boots', 17, 150, 3, 4, 300)
platinum_helm = Armour('Platinum Helmet', 23, 120, 4, 1, 475)
platinum_breastplate = Armour('Platinum Breastplate', 25, 100, 4, 2, 500)
platinum_pants = Armour('Platinum Pants', 24, 110, 4, 3, 495)
platinum_boots = Armour('Platinum Boots', 22, 150, 4, 4, 485)


class Weapon:
    def __init__(self, name, damage, solidity, level, price):
        self.name = name
        self.damage = damage
        self.solidity = solidity
        self.level = level
        self.type = 0
        self.price = price
        self.equippable = True


basic_sword = Weapon('Basic Sword', 15, 50, 0, 0)
bronze_broadsword = Weapon('Bronze Broadsword', 20, 100, 1, 100)
silver_broadsword = Weapon('Silver Broadsword', 30, 150, 1, 200)
gold_broadsword = Weapon('Gold Broadsword', 45, 80, 2, 300)
platinum_broadsword = Weapon('Platinum Broadsword', 60, 100, 2, 500)
bronze_battleaxe = Weapon('Bronze Battleaxe', 30, 150, 2, 150)
silver_battleaxe = Weapon('Silver Battleaxe', 50, 200, 2, 300)
gold_battleaxe = Weapon('Gold Battleaxe', 75, 100, 2, 500)
platinum_battleaxe = Weapon('Platinum Battleaxe', 100, 125, 3, 1000)


class Amulet:
    def __init__(self, damage, defense, healing, name, price):
        self.damage = damage
        self.defense = defense
        self.healing = healing
        self.price = price
        self.name = name
        self.type = 5
        self.level = 0
        self.equippable = True


null_amulet = Amulet(0, 0, 0, 'nothing', 0)
small_amulet_strength = Amulet(3, 0, 0, 'Small Amulet of Strength', 50)
medium_amulet_strength = Amulet(5, 0, 0, 'Medium Amulet of Strength', 100)
large_amulet_strength = Amulet(8, 0, 0, 'Large Amulet of Strength', 200)
small_amulet_defense = Amulet(0, 3, 0, 'Small Amulet of Defense', 50)
medium_amulet_defense = Amulet(0, 5, 0, 'Medium Amulet of Defense', 100)
large_amulet_defense = Amulet(0, 8, 0, 'Large Amulet of Defense', 200)
small_amulet_healing = Amulet(0, 0, 3, 'Small Amulet of Healing', 50)
medium_amulet_healing = Amulet(0, 0, 5, 'Medium Amulet of Healing', 100)
large_amulet_healing = Amulet(0, 0, 8, 'Large Amulet of Healing', 200)

# Dictionary is here because otherwise the objects are undefined
equipment_dict = {
    'Small Amulet of strength': small_amulet_strength,
    'Medium Amulet of strength': medium_amulet_strength,
    'Large Amulet of strength': large_amulet_strength,
    'Small Amulet of Defense': small_amulet_defense,
    'Medium Amulet of Defense': medium_amulet_defense,
    'Large Amulet of Defense': large_amulet_defense,
    'Small Amulet of Healing': small_amulet_healing,
    'Medium Amulet of Healing': medium_amulet_healing,
    'Large Amulet of Healing': large_amulet_healing,
    'Bronze Broadsword': bronze_broadsword,
    'Silver Broadsword': silver_broadsword,
    'Gold Broadsword': gold_broadsword,
    'Platinum Broadsword': platinum_broadsword,
    'Bronze Battleaxe': bronze_battleaxe,
    'Silver Battleaxe': silver_battleaxe,
    'Gold Battleaxe': gold_battleaxe,
    'Platinum Battleaxe': platinum_battleaxe,
}


class Potion:

    def __init__(self, name, effect, intensity):
        self.name = name
        self.effect = effect
        self.intensity = intensity
        self.level = 0
        self.price = intensity * 25
        self.equippable = False

    def use(self, target):
        print(f'You use your {self.name}')
        if self.effect == 0:
            player.health += 5 * self.intensity
            print(f'The {self.name} heals you {5 * self.intensity}')
        elif self.effect == 1:
            target.poison += self.intensity * 3
        elif self.effect == 2:
            target.health -= 5 * self.intensity
        elif self.effect == 3:
            target.damage -= self.intensity * 3
        else:
            player.invincibility = 1
        player.backpack.remove(self)


small_potion_healing = Potion("Small Potion of Healing", 0, 1,)
medium_potion_healing = Potion('Medium Potion of Healing', 0, 2)
large_potion_healing = Potion('Large Potion of Healing', 0, 3)
small_potion_poison = Potion('Small Potion of Poison', 1, 1)
medium_potion_poison = Potion('Medium Potion of Poison', 1, 2)
large_potion_poison = Potion('Large Potion of Poison', 1, 3)
small_potion_damage = Potion('Small Potion of Instant Damage', 2, 1)
medium_potion_damage = Potion('Medium Potion of Instant Damage', 2, 2)
large_potion_damage = Potion('Large Potion of Instant Damage', 2, 3)
small_potion_weakness = Potion('Small Potion of Weakness', 3, 1)
medium_potion_weakness = Potion('Medium Potion of Weakness', 3, 2)
large_potion_weakness = Potion('Large Potion of Weakness', 3, 3)
small_invincibility_potion = Potion('Small Potion of Invincibility', 4, 1)
medium_invincibility_potion = Potion('Medium Potion of Invincibility', 4, 2)
large_invincibility_potion = Potion('Large Potion of Invincibility', 4, 3)


class Player:
    def __init__(self, name, damage, mhealth, money):
        self.name = name
        self.damage = damage
        self.mhealth = mhealth
        self.health = mhealth
        self.money = money
        self.score = 0
        self.headwear = no_armour
        self.body_armour = no_armour
        self.pants = no_armour
        self.footwear = no_armour
        self.total_armour_class = 0
        self.backpack = [small_potion_weakness]
        self.bracelet1 = null_amulet
        self.bracelet2 = null_amulet
        self.necklace = null_amulet
        self.quiversize = 0
        self.equipped_weapon = basic_sword
        self.temp_damage = damage * self.equipped_weapon.damage
        self.bank_money = 0
        self.level = 1
        self.xp = 0
        self.invincibility = 0


print('Welcome to the dungeon of rickrollia!')
player = Player(input('What is your name, fellow adventurer?').title().lstrip(), 1, 500, 350)
t.sleep(1)
menu()
