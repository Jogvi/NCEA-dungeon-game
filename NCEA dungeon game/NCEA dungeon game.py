import time as t
import random as r
import pickle as p

delve_inputs=['yes','y','delve','d','deeper','deep']
home_inputs = ['h','home','back','b']
save_inputs= ['s','save']

class Lv1_ennemies:
    def __init__(self,name,damage,max_health):
        self.name=name
        self.damage=damage
        self.health=max_health
        self.max_health=max_health

goblin=Lv1_ennemies('goblin',5,20)
bat=Lv1_ennemies('bat',1,1)
skeleton=Lv1_ennemies('skeleton',8,10)

class Player:
    def __init__(self,name,damage,health,money):
        self.name=name
        self.damage=damage
        self.health=health
        self.money=money
print('Welcome to the dungeon of rickrollia!')
player=Player(input('What is your name, fellow adventurer?'),10,30,50)

def save(obj,file):
    slot=input('what save slot would you like to use?')
    if slot==1:
         save_file=Save1
    elif slot==2:
         save_file=Save2
    elif slot == 3:
         save_file=Save3
    p.dump( player, open( save_file, "wb" ) )

def load(file):
    import_result=p.load(open(file,'rb'))
    return import_result


    
    
def header():
    print('header')
    #do later

def menu():
    action=input(f'You now have {player.health} health points left. Would you like to delve'\
          'deeper in the dungeon, or go home?')
    if action in delve_inputs:
        delve()
    elif action in home_inputs:
        home()
    elif action in save_inputs:
        save
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
    player_damage=int((player.damage*r.randint(1,100)/100)+1)
    player.health-=damage
    monster.health-=player_damage
    print(f'The {monster.name} deals you {damage} damge')
    if player.health<=0:
        print('The {monster} kills you. This is the end of the tale of {player.name}')
        game_over()
    if monster.health>0:
        print(f'You retaliate, causing it {player_damage} damage! It now has {monster.health} hp left!')
        print(f'You have {player.health} hp left!')
        input('Press [Enter] to continue')
        fight(monster)
    else:
        print(f'The {monster.name} dies after you deal it {player_damage} damage')
        monster.health=monster.max_health
    menu()
def shop():
    print('shop')
    #do later
def healer():
    print('healer')
    #do later
menu()
