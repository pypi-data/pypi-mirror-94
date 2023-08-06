#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 22:28:49 2017

@author: albintveitankappi
"""
import escapetheforest.items
import escapetheforest.tiles

# Things to fix:
# LeaveForrestTile cant be in the middle of the forrest, thats silly! But then again, the person playing the game 
# would never need to explore the interior... If we didnt make it absolutely neccessary. 
# 
# We could have many findStickTiles but if we already have a stick or a sharpened stick in our inventory then we shouldnt 
# Be able to pick up a new one. They should be transformed into EmptyForrestTiles
# Im thinking its time to introduce an NPC that its possible to hold a conversation with! An old man in a hut? 
# A troll, at first appearing to be a stone?

import escapetheforest.world as world
import escapetheforest.player as player
#from escapetheforest.player import Player
import os
#print(os.getcwd())

def play():

    world.load_tiles()
    pc = player.Player()
    #The below line prints out all the attributes of the player
    #print(pc.__dict__)
    print("\n","====================THE FOREST ESCAPE========================")
    print("In this game you have two options. Escape the forest by finding the exit, or buy yourself out by selling mushrooms to the forest elf!")
    room = world.tile_exists(pc.location_x, pc.location_y)
    print(room.tile_text())
    global token
    token = 0

    #Game loop starts here:
    while pc.is_alive() and not pc.victory:
        for i in pc.inventory:
            #print(i)
            if isinstance(i, items.gold):
                if i.value >= 50:
                    print("You have gathered 50 coins and win the game!")
                    pc.victory = True

        room = world.tile_exists(pc.location_x, pc.location_y)

        if not token == 0:
            print(room.tile_text())
        token = 1
        room.modify_player(pc)
        #print("The _world dict tile instance on location {} is {}".format((pc.location_x, pc.location_y), room))

        if pc.is_alive() and not pc.victory:
            print("choose an action:\n")
            available_actions = room.available_actions(pc)
            for action in available_actions:
                print(action)
            action_input=input("Action: ")
            print("\n")
            for action in available_actions:
                if action_input == action.hotkey:
                    pc.do_action(action, **action.kwargs)
                    break
        
    if pc.is_alive() == False:
        print('You died a horrible death!')



           

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))

    os.chdir((os.path.dirname(os.path.realpath(__file__))))

    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))

    import escapetheforest.items as items
    import escapetheforest.world as world
    import escapetheforest.player as player

    play()
