


#   example map:
'''
######################################################
######################################################
######################################################
######################################################
######################################################
########      ##          A           ################
########G                             ################
########      ##   #             #    ################
################     B    C           ################
################                      ################
################   #             #    ################
################                      ################
################           D          ################
################   #             #    ################
################                      ################
################                      ################
################# ################## #################
################                      ################
################            E      F  ################
################                      ################
################                      ################
##########################  ##########################
##########################  ##########################

There are three rooms, room 1, 2, & 3. 
Room 2 is the largest, being 105 feet wide by 50 feet long. 
Along the east wall there are three pillars.
Along the west wall there are three pillars. 
In the middle of the north wall in room 2 is 'A'. 
10 feet south of 'A' is 'C'. 
20 feet west of 'C' is 'B'.
15 feet south and 5 feet east of 'C' is 'D'. 
North-west, connected through a central hallway to room 2, is room 3. 
Room 3 is 25 feet wide by 15 feet long. 
Along the west wall of room 3, there is 'G'.
South, connected through two hallways to room 2, is room 1. 
room 1 connects to the outside through a halway to the south.
In the middle of room 1 is 'E'.
Towards the east of room 1 is 'F'. 




'''



class room():
    ''' 
    Room is a class which encapsulates information about a room. 

    '''
    def __init__(self):
        self.width = 0
        self.length = 0
        self.height = 0

        self.adjoining=[] # This is a list of rooms & hallways connected to this room, along with directions

    def describe_room(self,room_name):
        description = room_name + "is "+str(self.width)+" feet wide by " + str(self.length) + "feet long, and "+str(self.height)+" feet tall.\n"
        
        for room, direction in self.adjoining:
            description += "To the "+direction+"is a " + "halway " if len(room.adjoining)==2 else "room " + ""




class map():
    def __init__(self):

        self.entities=[]
        
        self.terrain=[]
        self.rooms=[]
        

    def describe(self):
        
        rooms = 


         
        
        
