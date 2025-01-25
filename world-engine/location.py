import error_log as erlg
import character as *
import item as *


class location():

    def __init__():

        self.name=""
        self.description=""

        self.characters=[] # holds multiple characters
        self.items=[] # items in the location
        self.neighbors=[]


    def remove_character(character):
        if(character in self.characters):
            self.characters.remove(character)
        else:
            erlg.log("tried to remove " + character.name + ", but the character is not at " + self.name + ".")

    def add_character(character):
        if(character in self.characters):
            erlg.log("tried to add " + character.name + " to " + self.name + ", but the character is already there.")
        else:
            self.charactes.append(character)

    def has_character(character):
        if(is_instance(character, Character)):
            return character in self.characters;
        elif(is_instance(character, str)):
            for entry in self.characters:
                if entry.name == character:
                    return True
            return False
        else:
            raise TypeError


    def has_item(item):
        if(is_instance(item, Item)):
            return item in self.items
        elif(is_instance(item, str)):
            for entry in self.characters:
                if(entry.name == item):
                    return True
            return False
        else:
            raise TypeError



