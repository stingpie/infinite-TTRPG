import math as *
import error_log as erlg



class Character():

    def __init__():
        
        self.status=[]
        self.name=""
        self.description=""
        
        self.calories=1600# current calories
        self.cal_req = 67 # how many calories are expended per hour
        self.fat = 1 # pounds of fat. a pound of fat has 4100 calories.
        
        self.cycle={} # 0:home -> 6:farm -> 16:market -> 18:home 
        current_loc=0 # place holder
        
        inventory=[] # array of items this character holds

    def give_item(character, item):
        for entry in inventory:
            if(entry.name==item):
                character.inventory.append(entry)
                self.inventory.remove(entry)
                return
        erlg.log(self.name + " tried to give " + character.name + " a " + item + ", but it's not in their inventory.")

    def take_item(location, item):
        if(location.has_item(item)):
            self.inventory.append(location.remove_item(item))
        else:
            erlg.log(self.name + " tried to take " + item + " from " +location.name +", but it's not there.")

    def go_to(location):
        current_loc.remove_character(self)
        # TODO: add travel time
        location.add_character(self)

    def spend_time(period, intensity):
        self.calories -= period * intensity * self.cal_req
        if(self.calories<=0):
            self.calories += 4100 * ceil(self.calories / -4100)
        if(fat<0):
            self.kill()
        
    def kill():
        #do something.
        

