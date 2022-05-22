import time as t
import random as r
import pickle as p

delve_inputs=['yes','y','delve','d','deeper','deep']
home_inputs = ['h','home','back','b']

class Lv1_ennemies:
    def __init__(self,damage,hp):
        self.damage=damage
        self.hp=hp

goblin=Lv1_ennemies(5,10)
bat=Lv1_ennemies(1,1)
skeleton=Lv1_ennemies(8,5)

class Player:
    def __init__(self,name,damage,hp,money):
        self.name=name
        self.damage=damage
        self.hp=hp
        self.money=money
print('Welcome to the dungeon of rickrollia!')
player=Player(input('What is your name, fellow adventurer?'),15,30,50)

def header():
    print('header')
    #do later

def menu(hp):
    action=input(f'You now have {hp} health points left. Would you like to delve'\
          'deeper in the dungeon, or go home')
    if action in delve_inputs:
        delve(hp)
    elif action in home_inputs:
        home()
def delve(hp):
    print('delve')
    #do later
menu(player.hp)