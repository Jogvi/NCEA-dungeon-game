import time as t
import random as r
import pickle as p

delve_inputs=['yes','y','delve','d','deeper','deep']
home_inputs = ['h','home','back','b']

class Lv1_ennemies:
    def __init__(self,name,damage,health):
        self.name=name
        self.damage=damage
        self.health=health

goblin=Lv1_ennemies('goblin',5,10)
bat=Lv1_ennemies('bat',1,1)
skeleton=Lv1_ennemies('skeleton',8,5)

class Player:
    def __init__(self,name,damage,health,money):
        self.name=name
        self.damage=damage
        self.health=health
        self.money=money
print('Welcome to the dungeon of rickrollia!')
player=Player(input('What is your name, fellow adventurer?'),15,30,50)

def header():
    print('header')
    #do later

def menu():
    action=input(f'You now have {player.health} health points left. Would you like to delve'\
          'deeper in the dungeon, or go home')
    if action in delve_inputs:
        delve()
    elif action in home_inputs:
        home()
def delve():
    stage=r.randint(0,100)
    if stage<=90:
        monster=r.randint(1,3)
        if monster==1:
            fight(goblin)
        elif monster==2:
            fight(bat)
        elif monster==3:
            fight(skeleton)
    elif stage<=95:
        shop()
    elif stage<=99:
        healer()
    else:
        print('You enter an empty room...')
        menu(hp)
def fight(monster):
    player.health-=monster.damage
    monster.health-=player.damage
    damage=(monster.damage*r.randint(1,100)/100)+1
    player_damage=(player.damage*r.randint(1,100)/100)+1
    print(f'A wild {monster.name} appears!')
    print(f'The {monster.name} deals you {damage}')
    print(f'You retaliate, causing it {player_damage} damage! It now has {monster.health} hp left!')
def shop():
    print('shop')
    #do later
def healer():
    print('healer')
    #do later
menu()
