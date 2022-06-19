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
    5 : 'Stages\\Shop\\Trinkets_stocks.txt',
    6 : 'Stages\\Shop\\Potions_stocks.txt',
    7 : 'Stages\\Shop\\Amulets_stocks.txt',
    8 :'Stages\\Shop\\Enchantments_stocks.txt',
    9 : 'Stages\\Shop\\Bows_&_arrows_stocks.txt',
    }

item_types={
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
    global player
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
    player.temp_damage = player.damage * player.equipped_weapon.damage
    player.total_armour_class = player.headwear.armour+player.body_armour.armour\
                               +player.pants.armour+player.footwear.armour
    action = input(f'You now have {player.health} health points left. Would you like to delve '\
          'deeper in the dungeon, or go home? You can also choose to save by '\
          f'typing "{save_inputs[0]}" or "{save_inputs[1]}"'\
          f'and load with "{load_inputs[0]}" or "{load_inputs[1]}" \n')
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
    if stage<=0:
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
    player.temp_damage=int((player.temp_damage*r.randint(1,150)/100)+1)
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
    if item.type == 0:
        player.equipped_weapon = item
        menu()
    elif item.type == 1:
        player.headwear = item
        menu()
    elif item.type == 2:
        player.body_armour = item
        menu()
    elif item.type ==3:
        player.pants = item
        menu()
    elif item.type == 4:
        player.footwear = item
        menu()
    elif item.type==5:
        try:
            action=int(input(f'Would you like to equip your {item.name} as a '\
                         'right wrist bracelet(1), a left wrist bracelet(2) or'\
                         'a necklace(3)?'))
            if action>3:
                raise ValueError
        except ValueError:
            if player.bracelet1== null_amulet:
                equip_spot = "right bracelet"
                player.bracelet1 = item
            elif player.bracelet2== null_amulet:
                equip_spot = "left bracelet"
                player.bracelet2 = item
            elif player.necklace== null_amulet:
                equip_spot = "necklace"
                player.necklace = item
            print(f'oops. your bracelet will be equipped as a{equip_spot}')
        if action==1:
            player.bracelet1=item
            print(f"Your new right bracelet is a {player.bracelet1.name}")
        elif action==2:
            player.bracelet2=item
            print(f"Your new left bracelet is a {player.bracelet2.name}")
        elif action == 3:
            player.necklace=item
            print(f"Your new necklace is a {player.necklace.name}")
        menu()

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
def remove_charachter(item, remove):
    out = ""
    for i in range(0, len(item)): 
        if item[i] not in remove: 
            out = out + item[i]
        else:
            out = out + " "
    out = out.title()
    return out

def shop():
    shopkeeper_id=r.randint(10,19)
    shop_id=r.randint(1,9)
    shop_id=7
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
    #if shop is inferior to 3 it is a service
    if shop_id > 3:
        print('this is what we have on sale')
        shop_stock=stock_dict[shop_id]
        with open(shop_stock,'r') as f:
            content=f.readlines()

            
        items_on_sale=[]
        loop = 0
        while loop <3:
            item = content[r.randint(0,len(content)-1)].strip()
            if eval(item).level<=player.level:
                items_on_sale.append(item)
                print(f'{loop+1}:{eval(item).name} : {eval(item).price}')
                loop+=1
        action=input('Would you like to buy something?You currently have '\
                     f'{player.money} Ducats \n')
        if action in yes_inputs:
            good = False
            while not good:
                action=int(input('What would you like to buy? (1,2 or 3)\n'))
                global item_bought
                try:
                    item = items_on_sale[action-1]
                    good = True
                except IndexError:
                    print('oops')
            item = eval(item_bought)
            if item.price <= player.money:
                player.money-=item.price
                action=input(f'Do you want to equip your new {item.name}? \n')
                if action in yes_inputs:
                    equip_item(item)
                elif action in no_inputs:
                    player.backpack.append(item)
                else:
                    print("I think you've misspelled your input")
            else:
                print('sorry, you dont have enough money...')
                shop()
        else:
            print('See you soon!')
            menu()
    else:
        action=input('Would you like to use our services?'\
                     f'You currently have {player.money} Ducats \n')
        if action in yes_inputs:
            print('Services will be available soon')
            menu()
def healer():
    print('healer')
    #do later
    menu()

def game_over():
    action=input('would you like to save your score and name? \n')
    if action in yes_inputs:
        with open('Save_Files\\Saved_Scores.txt','r') as f:
            content = f.readlines()
        with open('Save_Files\\Saved_Scores.txt','w') as f:
            f.write(' '.join(content))
            f.write('\n')
            f.write(str(player.score).strip())
            f.write('\n')
            f.write(player.name.strip())

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

class Armour:
    def __init__(self, name, armour, solidity, level, item_type, price):
        self.name = name
        self.armour = armour
        self.solidity = solidity
        self.level = level
        self.type = item_type
        self.price = price
null_armour = Armour("nothing", 0, 0, 0, 0, 0)
sweaty_underpants = Armour("Sweaty Underpants", 1, 69, 0, 3,1)
bucket = Armour("Bucket", 3,50,0,1,35)
leather_breastplate = Armour("Leather Breastplate", 5, 100, 1, 2,50)
leather_pants = Armour("Leather Pants", 5, 90, 1, 3, 40)
#leather_boots
#bronze_helm
#bronze_breastplate
#bronze_pants
#bronze_boots
#silver_helm
#silver_breastplate
#silver_pants
#silver_boots
#gold_helm
#gold_breastplate
#gold_pants
#gold_boots
#platinum_helm
#platinum_breastplate
#platinum_pants
#platinum_boots

class Weapon:
    def __init__(self,name,damage,solidity, level,price):
        self.name=name
        self.damage=damage
        self.solidity=solidity
        self.level = level
        self.type = 0
        self.price = price
basic_sword = Weapon('Basic Sword',15,50, 0,0)
bronze_broadswoard = Weapon('Bronze Broadswoard' , 20,  100,1,100)
silver_broadswoard = Weapon('Silver Broadswoard', 30, 150,1,200)
gold_broadswoard = Weapon('Gold Broadswoard', 45, 80,2,300)
platinum_broadswoard = Weapon('Platinum Broadswoard',60,100,2,500)
bronze_battleaxe = Weapon('Bronze Battleaxe',30,150,2,150)
silver_battleaxe = Weapon('Silver Battleaxe',50,200,2,300)
gold_battleaxe = Weapon('Gold Battleaxe', 75, 100, 2,500)
platinum_battleaxe = Weapon('Platinum Battleaxe',100,125,3,1000)    

class Amulet:
    def __init__(self,damage,defense,healing,name, price):
        self.damage=damage
        self.defense=defense
        self.healing=healing
        self.price = price
        self.name=name
        self.type = 5
        self.level = 0

null_amulet=Amulet(0,0,0,'nothing',0)
small_amulet_strength=Amulet(3,0,0,'Small Amulet of Strength',50)
medium_amulet_strength=Amulet(5,0,0,'Medium Amulet of Strength',100)
large_amulet_strength=Amulet(8,0,0,'Large Amulet of Strength',200)
small_amulet_defense=Amulet(0,3,0,'Small Amulet of Defense',50)
medium_amulet_defense=Amulet(0,5,0,'Medium Amulet of Defense',100)
large_amulet_defense=Amulet(0,8,0,'Large Amulet of Defense',200)
small_amulet_healing=Amulet(0,0,3,'Small Amulet of Healing',50)
medium_amulet_healing=Amulet(0,0,5,'Medium Amulet of Healing',100)
large_amulet_healing=Amulet(0,0,8,'Large Amulet of Healing',200)

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
    'Bronze Broadswoard' : bronze_broadswoard,
    'Silver Broadswoard' : silver_broadswoard,
    'Gold Broadswoard' : gold_broadswoard,
    'Platinum Broadswoard' : platinum_broadswoard,
    'Bronze Battleaxe' : bronze_battleaxe,
    'Silver Battleaxe' : silver_battleaxe,
    'Gold Battleaxe' : gold_battleaxe,
    'Platinum Battleaxe' : platinum_battleaxe,
}

class Player:
    def __init__(self,name,damage,health,money):
        self.name=name
        self.damage=damage
        self.health=health
        self.money=money
        self.score=0
        self.headwear=null_armour
        self.body_armour=null_armour
        self.pants=null_armour
        self.footwear=null_armour
        self.total_armour_class=0
        self.backpack=[]
        self.bracelet1=null_amulet
        self.bracelet2=null_amulet
        self.necklace=null_amulet
        self.quiversize=0
        self.equipped_weapon = basic_sword
        self.temp_damage=damage*self.equipped_weapon.damage
        self.bank_money=0
        self.level=1

print('Welcome to the dungeon of rickrollia!')
player=Player(input('What is your name, fellow adventurer?').title().lstrip(),1,50,350)

menu()





