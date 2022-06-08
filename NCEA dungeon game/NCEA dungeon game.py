import random as r
import pickle as p

yes_inputs=['yes','y','yea','yeah','yep','yesaroo']
no_inputs=['no','n','nope','back','b','cancel','c']
delve_inputs=['yes','y','delve','d','deeper','deep']
home_inputs = ['h','home','back','b']
save_inputs= ['s','save']
load_inputs=['l','load']
equipable= [1,2,3,4,5]

item_bought= ''

slot_dict={
    1:'Save_Files\\Save1.pkl',
    2:'Save_Files\\Save2.pkl',
    3:'Save_Files\\Save3.pkl'
    }
stock_dict = {
    4 : 'Stages\\Shop\\Trinkets_stocks.txt',
    5 : 'Stages\\Shop\\Potions_stocks.txt',
    6 : 'Stages\\Shop\\Amulets_stocks.txt',
    7 :'Stages\\Shop\\Enchantments_stocks.txt',
    8 : 'Stages\\Shop\\Weaponsmith_stocks.txt',
    9 : 'Stages\\Shop\\Bows_&_arrows_stocks.txt',
    10 : 'Stages\\Shop\\Forge_stocks.txt',
    }

price_dict={
    'Small Amulet of strength' : 50,
    'Medium Amulet of strength'  :100,
    'Large Amulet of strength' : 200,
    'Small Amulet of Defense' : 50,
    'Medium Amulet of Defense' : 100,
    'Large Amulet of Defense' : 200,
    'Small Amulet of Healing' : 100,
    'Medium Amulet of Healing':200,
    'Large Amulet of Healing':200,
    }

item_types={
    'Small Amulet of strength' :  5,
    'Medium Amulet of strength': 5,
    'Large Amulet of strength' : 5,
    'Small Amulet of Defense' : 5,
    'Medium Amulet of Defense' : 5,
    'Large Amulet of Defense' : 5,
    'Small Amulet of Healing' : 5,
    'Medium Amulet of Healing' : 5,
    'Large Amulet of Healing' : 5,
    'Shortbow':6,
    'Bow' : 6,
    'Longbow':6,
    '10 arrows':7,
    '50 arrows':7,
    '100 arrows':7,
    '5 Fire Arrows':7,
    'Small quiver':8,
    'Medium quiver':8,
    'Large quiver':8,
    }
     
def save_game():
    try:
        slot=int(input('what save slot would you like to use?'))
    except ValueError:
        print('Sorry, that is not a valid slot...')
        save_game()
    save_file='Save_Files\\Save1.pkl'
    if slot==1:
        save_file='Save_Files\\Save1.pkl'
    elif slot==2:
        save_file='Save_Files\\Save2.pkl'
    elif slot == 3:
        save_file='Save_Files\\Save3.pkl'
    p.dump( player, open(save_file, "wb" ) )
    print(f'you have succesfully saved {player.name} in slot {slot}!')
 
def save(obj,file):
    p.dump(obj,open(file,'wb'))
    
def load(file):
    with open(file,'rb') as data:
        obj=p.load(data)
    return obj
 
def load_game():
    slot=slot_dict[int(input('What slot would you like to load?'))]
    with open(slot, 'rb') as data:
        player = p.load(data)
    return player

def home():
    print('end of the game')
    
def header():
    print('header')
    #do later

def menu():
    global player
    player.damage*=player.equipped_weapon.damage
    player.total_armour_class=player.headwear+player.body_armour+player.pants+player.footwear
    action=input(f'You now have {player.health} health points left. Would you like to delve '\
          'deeper in the dungeon, or go home? You can also choose to save by '\
          f'typing "{save_inputs[0]}" or "{save_inputs[1]}"'\
          f'and load with "{load_inputs[0]}" or "{load_inputs[1]}"')
    if action in delve_inputs:
        delve()
    elif action in home_inputs:
        home()
    elif action in save_inputs:
        save_game()
    elif action in load_inputs:
        player=load_game()
        print(f'You have loaded {player.name}')
        menu()
    else:
        menu()
def delve():
    stage=r.randint(0,100)
    if stage<=90:
        monster=r.randint(1,3)
        if monster==1:
            print(f'A wild {goblin.name} appears!')
            fight(goblin)
        elif monster==2:
            print(f'A wild {bat.name} appears!')
            fight(bat)
        elif monster==3:
            print(f'A wild {skeleton.name} appears!')
            fight(skeleton)
    elif stage<=95:
        shop()
    elif stage<=99:
        healer()
    else:
        print('You enter an empty room...')
        menu()
        
def fight(monster):
    damage=int(monster.damage*(r.randint(1,100)/100+1))
    player.temp_damage=int((player.damage*r.randint(1,100)/100)+1)
    player.health-=damage
    monster.health-=player.temp_damage
    print(f'The {monster.name} deals you {damage-player.total_armour_class} damage')
    if player.health<=0:
        print(f'The {monster.name} kills you. This is the end of the tale of {player.name}')
        game_over()
    else:     
        if monster.health>0:
            print(f'You retaliate, causing it {player.temp_damage} damage! It now has {monster.health} hp left!')
            print(f'You have {player.health} hp left!')
            input('Press [Enter] to continue')
            fight(monster)
        else:
            print(f'The {monster.name} dies after you deal it {player.temp_damage} damage')
            player.score+=monster.level
            monster.health=monster.max_health
            player.money+=monster.money
            if monster.level==1:
                print(f'The {monster.name} dropped {monster.money} copper pieces')
            menu()
def equip_item(item):
    if item_types[item]==1:
        player.headwear=armour_dict[item]
    elif item_types[item]==2:
        player.body_armour=armour_dict[item]
    elif item_types[item]==3:
        player.pants=armour_dict[item]
    elif item_types[item]==4:
        player.footwear=armour_dict[item]
    elif item_types[item]==5:
        action=int(input(f'Would you like to equip your {item} as a '\
                     'right wrist bracelet(1), a left wrist bracelet(2) or'\
                     'a necklace(3)?'))
        if action==1:
            player.bracelet1=equipment_dict[item]
            print(f"Your new right bracelet is a {player.bracelet1.name}")
        elif action==2:
            player.bracelet2=equipment_dict[item]
            print(f"Your new left bracelet is a {player.bracelet2.name}")
        elif action == 3:
            player.necklace=equipment_dict[item]
            print(f"Your new necklace is a {player.necklace.name}")

def bank():
    if input('would you like to use our services?') in yes_inputs:
        action = int(input('What would you like to do? (1:Deposit; 2:Withdrawal, 3:Borrow money'))
        if action==1:
            deposit_amount=int(input('How much would you like to deposit?'))
            if deposit_amount<= player.money:
                if input('You are about to deposit {deposit_amount}. Are you sure?') in yes_inputs:
                    player.money-=deposit_amount
                    player.bank_money+=deposit_amount
                else:
                    bank()
            else:
                print('I would love to relieve you of **that** amount, but you do not have enough money...')
                input('[Enter] to continue')
                bank()
        elif action==2:
             if player.money_bank ==0:
                 print("You don't even have money here! Please deposit before you start withdrawing...")
             withdrawal_amount=int(input("how much would you like to withdraw"))
             if withdrawal_amount<=player.bank_money:
                player.bank_money-=player.bank_money
            else:
                if player.bank_money>0:
                    print(f'Sorry, your bank account only has {player.bank_money} ducats')
                               

def shop():
    shopkeeper_id=r.randint(10,19)
    shop_id=r.randint(1,9)
    shop_id=6
    with open('Stages\\Shop\\Shops.txt','r') as f:
        content=f.readlines()
        shop_name=content[shop_id-1].strip()
        shopkeeper=content[shopkeeper_id].strip()
    with open('Stages\\Shop\\Shop_Descriptions.txt','r') as f:
        content=f.readlines()
        shop_description = content[shop_id-1]
    print(f"welcome to {shopkeeper}'s {shop_name}. I am {shopkeeper}.")
    print(shop_description)
    input('Press [Enter] to continue')
    if shop_id > 3:
        print('this is what we have on sale')
        shop_stock=stock_dict[shop_id]
        with open(shop_stock,'r') as f:
            content=f.readlines()
        items_on_sale=[]
        for i in range (0,3):
            items_on_sale.append(content[r.randint(0,len(content)-1)].strip())
        for i in range (0,len(items_on_sale)):
            print(items_on_sale[i],':',price_dict[items_on_sale[i]])
        action=input('Would you like to buy something?You currently have '\
                     f'{player.money} Ducats')
        if action in yes_inputs:
            action=int(input('What would you like to buy? (1,2 or 3)'))
            global item_bought
            item_bought=items_on_sale[action-1]
            item_price=price_dict[item_bought]
            if item_price <= player.money:
                player.money-=item_price
                action=input(f'Do you want to equip your new {item_bought}?')
                if action in yes_inputs:
                    equip_item(item_bought)
                elif action in no_inputs:
                    player.backpack.append(item_bought)
                else:
                    print("I think you've misspelled your input")
            else:
                print('sorry, you dont have enough money...')
                menu()
        else:
            print('See you soon!')
            menu()
    else:
        action=input('Would you like to use our services?'\
                     f'You currently have {player.money} Ducats')
        if action in yes_inputs:
            print('Services will be available soon')
            menu()
def healer():
    print('healer')
    #do later
    menu()

def game_over():
    action=input('would you like to save your score and name?')
    if action in yes_inputs:
        with open('Save_Files\\Saved_Scores.txt','w') as f:
            f.write(str(player.score))
            f.write('\n')
            f.write(player.name)

class Lv1_ennemies:
    def __init__(self,name,damage,max_health,money):
        self.name=name
        self.damage=damage
        self.health=max_health
        self.max_health=max_health
        self.level=1
        self.money=money

goblin=Lv1_ennemies('goblin',5,20,5)
bat=Lv1_ennemies('bat',1,1,1)
skeleton=Lv1_ennemies('skeleton',8,10,10)

class Weapon:
    def __init__(self,name,damage,solidity, level):
        self.name=name
        self.damage=damage
        self.solidity=solidity
        self.level = level
basic_sword = Weapon('Basic Sword',15,50, 0)
bronze_broadswoard = Weapon('Bronze Broadswoard' , 20,  100,1)
silver_broadswoard = Weapon('Silver Broadswoard', 30, 150,1)
gold_broadswoard = Weapon('Gold Broadswoard', 45, 80,2)
platinum_broadswoard = Weapon('Platinum Broadswoard', 60 , 100,2)
bronze_battleaxe = Weapon('Bronze Battleaxe', 30,  150, 2)
silver_battleaxe = Weapon('Silver Battleaxe', 50, 200,2)
gold_battleaxe = Weapon('Gold Battleaxe', 75, 100, 2)
platinum_battleaxe = Weapon('Platinum Battleaxe',100,125,3)

class Amulet:
    def __init__(self,damage,defense,healing,name):
        self.damage=damage
        self.defense=defense
        self.healing=healing
        self.name=name

null_amulet=Amulet(0,0,0,'nothing')
small_amulet_strength=Amulet(3,0,0,'Small Amulet of Strength')
medium_amulet_strength=Amulet(5,0,0,'Medium Amulet of Strength')
large_amulet_strength=Amulet(8,0,0,'Large Amulet of Strength')
small_amulet_defense=Amulet(0,3,0,'Small Amulet of Defense')
medium_amulet_defense=Amulet(0,5,0,'Medium Amulet of Defense')
large_amulet_defense=Amulet(0,8,0,'Large Amulet of Defense')
small_amulet_healing=Amulet(0,0,3,'Small Amulet of Healing')
medium_amulet_healing=Amulet(0,0,5,'Medium Amulet of Healing')
large_amulet_healing=Amulet(0,0,8,'Large Amulet of Healing')

#Dictionnary is here because otherwhise the objects are undefined
equipment_dict={
    'Small Amulet of strength': small_amulet_strength,
    'Medium Amulet of strength':medium_amulet_strength,
    'Large Amulet of strength':large_amulet_strength,
    'Small Amulet of Defense':small_amulet_defense,
    'Medium Amulet of Defense': medium_amulet_defense,
    'Large Amulet of Defense':large_amulet_defense,
    'Small Amulet of Healing':small_amulet_healing,
    'Medium Amulet of Healing':medium_amulet_healing,
    'Large Amulet of Healing':large_amulet_healing,
}

class Player:
    def __init__(self,name,damage,health,money):
        self.name=name
        self.damage=damage
        self.health=health
        self.money=money
        self.score=0
        self.headwear=0
        self.body_armour=0
        self.pants=0
        self.footwear=0
        self.total_armour_class=0
        self.backpack=[]
        self.bracelet1=null_amulet
        self.bracelet2=null_amulet
        self.necklace=null_amulet
        self.quiversize=0
        self.equipped_weapon = basic_sword
        self.temp_damage=damage*self.equipped_weapon.damage
        self.bank_money=0
        
print('Welcome to the dungeon of rickrollia!')
player=Player(input('What is your name, fellow adventurer?'),1,50,50)

menu()
