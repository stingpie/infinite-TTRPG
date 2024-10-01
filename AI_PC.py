
import json, re
from utils import history_to_chat, append_status, prepend_character_info, complete_chat

class player():
    def __init__(self, client, model, name, json_, setting,  remind_status=False):
        self.name=name
        self.client = client
        self.model=model
        
        if(json_):
            state = json.loads(json_)

            self.character_name = state['name']
            self.description = state['description']
            if("appearance" in state):
                self.appearance = state['appearance']
            else:
                self.appearance = state['description']
            self.backstory=state['backstory']
            self.personality = state['personality']
            self.tags = state['tags']
            self.languages = state['languages']
            self.inventory= state['inventory']
        
        self.remind_status = remind_status
        self.setting = setting
        self.arbiter=None


    def take_turn(self, history):
        #print(self.name) 
        if(self.name.startswith("player")):
            return {'role':self.character_name, 'content':self.character_name+":\n"+input("What do you do, "+self.character_name+"? ")}

        _history = history.copy()

        chat = history_to_chat(_history, self.name if not self.character_name else self.character_name)
        chat = prepend_character_info(chat, self, self.setting)

        if(self.remind_status):
            chat = append_status(chat, self)

        limit=5
        while ( limit==5 or ( (not response.startswith(self.character_name)) and ":" in response and len(response.split(":")[0].split(" "))<5)  ): ##lazy way to 
            response = complete_chat(self.client, self.model, chat, arbiter=self.arbiter)

            speaker = re.search("^\s*(\S+\s*){1,4}:\n", response)
            #print(response)
            if(speaker and speaker.group(0)[:-1] == self.name):
                next_speaker = re.search("\n\s*(\S+\s*){1,4}:\n", response)
                if(next_speaker):
                    arbiter.append_to_stack(next_speaker.group(0)[:-2].strip())
                    response = response[:next_speaker.start(0)]
            else:
                limit-=1
                if limit==0:
                    break
                    response = None 


        response = {"role":self.character_name,"content":response}
        
        if(not response['content'].startswith(self.character_name+": ")):
            response['content'] = self.character_name + ": \n" + response['content']
        
        #response={"role":"scooby doo", "content":"YABADABADOO, SCOOBY DOOO"} 
       

        #print(response)

        return response


        


        













