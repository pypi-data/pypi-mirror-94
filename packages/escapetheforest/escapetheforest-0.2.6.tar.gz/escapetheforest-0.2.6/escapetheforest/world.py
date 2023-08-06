"""This is the actual world """

import escapetheforest.tiles as tiles
import random
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
map_file = os.path.join(THIS_FOLDER, 'map.txt')

_world = {}
starting_position = (0, 0)

#Now, this function goes through the map tile and creates a dictionary that contains the coordinates and the tile name


def load_tiles():
    """Parses a file that describes the world space into the _world object"""
    with open(map_file, "r") as f:
        rows = f.readlines()    #This is a variable that contains a number of rows,
                                # where each row is just a string containing all the information on each row in the "map.txt".
                                #This means that each row contains tile names as well as codes indicating tabs and new lines.
  #      row=[]

# the following lines takes each row of the map.txt file and appends them to a long list. Then it shuffles the list randomly and then it
# creates a new list with all the tiles randomly shuffled.

  #      for i in range(len(rows)):
  #          row.extend(rows[i].replace('\n','').split('\t'))
  #          #print(rows[i])
  #          #print(row)
  #          random.shuffle(row)
  #          val=0
  #          row2=[]
  #          while val<len(row):
  #              row2.append('\t'.join(row[val:val+4])+'\n')
  #              #print(row2)
  #              val+=4
  #  rows=row2

    #print(rows)
    #print(type(rows))
    x_max = len(rows[0].split('\t')) # This creates a variable x_max that is a number which is based on the length of the first row in the "rows" variable when splitting it on "/t/".
                                        ## This assumes all rows contain the same number of tabs.

    for y in range(len(rows)):  # For the whole length of the rows variable:
        cols = rows[y].split('\t')  #Split each row into a number of columns, by using the "/t" or tab command.
        #print(cols)

        for x in range(x_max):  # For the length of each row:
            tile_name = cols[x].replace('\n', '') # Create a new variable "tile_name" that contains the tilename in each column positon,
                                                    # where each newline indication "/n/" has been replaced with nothing ''.
                                                    #This basically cleans out so that only the clean tilename will be the current value of "tile_name" variable
                                                    # Windows users may need to replace '\r\n'

            #This just says that if the tile_name is startingroom, that should be our starting position.
            # The Starting_position variable is global so it can replace the value of the variable established in the beginning of this module.
            if tile_name == 'startingRoom':
                global starting_position
                starting_position = (x, y)

            #The variable _world is a dictionary that maps a coordinate pair to a tile. So the code _world[(x, y)]=....
            #creates the key (i.e. the coordinate pair) of the dictionary. If the cell is
            #an empty string, we don’t want to store a tile in it’s place which is why we have the code None if tile_name == ''.
            #However, if the cell does contain a name, we want to actually create a tile of that type. The getattr method is
            #built into Python and lets us reflect into the tile module and find the class whose name matches tile_name.
            #Finally the (x, y) passes the coordinates to the constructor of the tile.

            _world[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)

            if tile_name == '':
                _world[(x,y)] = None

            else:
                _world[(x, y)] = getattr(__import__('tiles'), tile_name)(x, y)



"""
    rlist=[0, len(rows)-1]
    print(rlist)

    print(rows)
    for key, value in _world.items():
        if(isinstance(value, tiles.leaveForrestTile)):
            print(key,value)
            print(key[0])
            if (key[1] != 0) and (key[1] != len(rows)-1):
                print("boo")
                nkey = (random.randint(0,3),random.choice(rlist))
                print(nkey)
                _world[key]= _world[nkey]
                print(_world[key])
                print(_world[nkey])
                print(_world)
                """








def emptify_tile(x,y):
    _world[(x, y)] = tiles.emptyForrestTile(x, y)
    return _world[(x, y)]


def tile_exists(x,y):
    """Returns the tile at the given coordinates or None if there is no tile.
    :param x: the x-coordinate in the worldspace
    :param y: the y-coordinate in the worldspace
    :return: the tile at the given coordinates or None if there is no tile
    """
    return _world.get((x,y))
