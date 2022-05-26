import time as t
import random as r
import pickle as p


yes_inputs=['yes','y','yea','yeah','yep','yesaroo']
delve_inputs=['yes','y','delve','d','deeper','deep']
home_inputs = ['h','home','back','b']
save_inputs= ['s','save']
load_inputs=['l','load']

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

def save(obj):
    try:
        slot=int(input('what save slot would you like to use?'))
    except ValueError:
        print('Sorry, that is not a valid slot...')
        save(obj)
    save_file='Save_Files\\Save1.pkl'
    if slot==1:
        save_file='Save_Files\\Save1.pkl'
    elif slot==2:
        save_file='Save_Files\\Save2.pkl'
    elif slot == 3:
        save_file='Save_Files\\Save3.pkl'
    p.dump( obj, open( save_file, "wb" ) )
    print(f'you have succesfully saved {obj.name} in slot {slot}!')
    
def load():
    slot=slot_dict[int(input('What slot would you like to load?'))]
    with open('Save_Files\\Save1.pkl', 'rb') as data:
        obj = p.load(data)
    return obj

def home():
    print('end of the game')
    
def header():
    print('header')
    #do later

def menu():
    global player
    action=input(f'You now have {player.health} health points left. Would you like to delve '\
          'deeper in the dungeon, or go home? You can also choose to save by '\
                 f'typing "{save_inputs[0]}" or "{save_inputs[1]}"    and load with "{load_inputs[0]}" or "{load_inputs[1]}"')
    if action in delve_inputs:
        delve()
    elif action in home_inputs:
        home()
    elif action in save_inputs:
        save(player)
    elif action in load_inputs:
        player=load()
        print(f'You have loaded {player.name}')
def delve():
    stage=r.randint(0,100)
    if stage<=9:
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
    player_damage=int((player.damage*r.randint(1,100)/100)+1)
    player.health-=damage
    monster.health-=player_damage
    print(f'The {monster.name} deals you {damage-player.total_armour_class} damage')
    if player.health<=0:
        print(f'The {monster.name} kills you. This is the end of the tale of {player.name}')
        game_over()
    else:     
        if monster.health>0:
            print(f'You retaliate, causing it {player_damage} damage! It now has {monster.health} hp left!')
            print(f'You have {player.health} hp left!')
            input('Press [Enter] to continue')
            fight(monster)
        else:
            print(f'The {monster.name} dies after you deal it {player_damage} damage')
            player.score+=monster.level
            monster.health=monster.max_health
            menu()
def shop():
    shopkeeper_id=r.randint(10,19)
    shop_id=r.randint(0,9)
    with open('Stages\\Shop\\Shops.txt','r') as f:
        content=f.readlines()
        shop_name=content[shop_id-1].strip()
        shopkeeper=content[shopkeeper_id].strip()
    with open('Stages\\Shop\\Shop_Descriptions.txt','r') as f:
        content=f.readlines()
        shop_description = content[shop_id-1]
    print(f"welcome to {shopkeeper}'s {shop_name}. I am {shopkeeper}.")
    print(shop_description)   
    if shop_id > 3:
        print('this is what we have on sale')
        shop_stock=stock_dict[shop_id]
        with open(shop_stock,'r') as f:
            content=f.readlines()
        items_on_sale=[]
        for i in range (0,3):
            items_on_sale.append(content[r.randint(0,len(content)-1)].strip())
        for i in range (0,len(items_on_sale)):
            print(items_on_sale[i])
        action=input('would you like to buy something?')
    else:
        action=input('Would you like to use our services?'\
                     f'You currently have {player.copper_pieces} copper pieces,'\
                     f'{player.silver_pieces} silver pieces and {player.gold_pieces} gold '\
                     'pieces')
    if action in yes_inputs:
        print('buy process strated')
        menu()
def healer():
    print('healer')
    #do later
    menu()

def game_over():
    action=input('would you like to save your score and name?')
    if save in yes_inputs:
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

class Player:
    def __init__(self,name,damage,health,money):
        self.name=name
        self.damage=damage
        self.health=health
        self.copper_pieces=money
        self.silver_pieces=0
        self.gold_pieces=0
        self.score=0
        self.headwear=0
        self.body_armour=0
        self.pants=0
        self.footwear=0
        self.total_armour_class=0
        
print('Welcome to the dungeon of rickrollia!')
player=Player(input('What is your name, fellow adventurer?'),15,50,50)

menu()

