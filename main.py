###################
## AI TTRPG MAIN ##
################### 


# 1) initial setup (ask user for stuff)
# 2) orchestator.narrate()
# 3) apply function calls
# 4) arbiter.choose().take_turn()
# 5) repeat 4 if desired
# 6) repeat 2-6


import os, random, arbiter, AI_PC, arbiter, orchestrator, character_to_json, ast



names = ["dave", "bill", "joel", "ted", "gary", "sheila", "amy", "jessica", "alice", "sally"]




class RPG():
    def __init__(self, client = None, model = 'gpt-4o-mini', world = "lore/simple-setting", character_path=None, remind_status = False, human_characters=[], player_narrator=False):

        if(client == None and model.startswith("gpt")):
            from openai import OpenAI as openai
        elif(client == None and model.startswith("claude")):
            from anthropic import Anthropic as openai

        self.client = openai()
        self.model = model

        if(character_path == None): ## pick three random characters from the player_characters & any subdir.
            
            files = [os.path.join("player_characters",f) for f in os.listdir("player_characters") if (os.path.isfile(os.path.join("player_characters",f)) and f.endswith(".txt") ) ]
            random.shuffle(files)
            character_path = files[:3]
        else:
            files = character_path
        


        character_jsons = [character_to_json.jsonify(openai(), character, model) for character in character_path]
        
        random.shuffle(names)


        self.characters = [AI_PC.player(self.client, self.model,names[i], character_jsons[i], os.path.join(world, "setting.txt"), remind_status ) for i in range(len(character_jsons))]
        
        if(human_characters):
            i=0
            for human in human_characters:
                for character in self.characters:
                    print(human, character.character_name)
                    if(character.character_name.startswith(human)):
                        character.name = "player"+str(i)
                        i+=1

        self.arbiter = arbiter.arbiter(self.characters, choose = "smart")
        z = {'name':[char.character_name for char in self.characters], 'desc':files[:len(character_path)]}
        self.narrator = orchestrator.orchestrator(openai(), self.model, "prompts/narrator.txt", os.path.join(world, "setting.txt"), tools=None, characters = z)
        
        self.narrator.is_player = player_narrator


        self.history=[]


        self.count=0#len(self.characters)
         



    def step(self, command):
       
        
        if(command.startswith("c") or command.startswith("cont")):
            
            
            
            if( not self.arbiter.narrators_turn and (self.narrator.is_player or self.count !=0  or (self.arbiter.choose == self.arbiter.smart and len(self.arbiter.char_stack)>0))):
                self.count-=1
                
            

                response = self.arbiter.choose().take_turn(self.history.copy()) 
                
                if(response['content']):
                    self.history.append(response)
                else:
                    self.arbiter.narrators_turn = True
    
            else:
                self.count=len(self.characters)
                self.history += self.narrator.narrate(self.history.copy())
                self.arbiter.narrators_turn=False

        elif(command == "u" or command.startswith("undo")):
            self.history = self.history[:-1]
            self.count = (self.count+1) % (len(self.characters)+1)
        elif(command.startswith("n ") or command.startswith("narrate")):
            self.history.append({'role':'narrator','content':"narrator:\n"+" ".join(command.split(" ")[1:])})
        elif(command == "+"):
            self.count = (self.count * 2 - 1) % (len(self.characters)+1)
        elif(command == "-"):
            self.count = (self.count+1) % (len(self.characters)+1)
        elif(command == "l" or command.startswith("list")):
            response = ""
            i=0
            for line in self.history:
                response += "{0:>4}".format(i) + " " + line['role'] +": " + line['content'].replace("\n","").replace("**","").replace(line['role']+":","")[:80]+"\n"
                i+=1
            return response
        elif(command == "h" or command.startswith("help")):
            return "Welcome to ITTRPG. This is a command-line RPG. \nCommands:\n c: continue.\n u: undo\n n: say something as narrator\n h: help\n l: list history\n load: load a campaign\n save: save a campaign\n [character name or 'narrator']: get that character or the narrator to say something."
        elif(command == "s" or command.startswith("save")):
            open(command.split(" ")[1],'w').write(str(self.history))
        elif(command.startswith("load") ):
            self.history=ast.literal_eval(open(command.split(" ")[1],'r').read())
            new_history=[]
            for line in self.history:
                if not line['content'].strip()=="narrator:":
                    new_history.append(line)
            self.history = new_history            


        elif(len(command)>=4): # directly call character
            if(command=="narrator"):
                self.history+=self.narrator.narrate(self.history.copy())
            else:
                for char in self.arbiter.characters:
                    if char.character_name.startswith(command):
                        self.history.append(char.take_turn(self.history))
                        break


        return self.history[-1]['content']





