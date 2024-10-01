
import ast, AI_PC, toolcalls
from utils import history_to_chat

class orchestrator():   ## This class is made to act as the narrator, or DM. 
    def __init__(self, client, model, prompt, setting,  tools, characters=None, is_player=False):
        self.client = client
        self.model = model
        self.prompt = open(prompt,'r').read()
        self.is_player=is_player

        if(tools!=None):
            self.tools = ast.literal_eval(open(tools,'r').read())

        self.setting=setting
       
        
        self.characters= characters
        #print("CHARACTERS",characters)

        #self.player = AI_PC.player(client, model, "narrator", None, setting )
        #self.player.description=open("prompts/narrator.txt",'r').read()
        #self.player.character_name="narrator"



    def narrate(self, history):
        

        if(self.is_player):
            return {'role':'narrator', 'content':"narrator:\n"+input("What happens next, narrator?")}



        chat = history_to_chat(history, "narrator", include_tool_calls=True)
        
       # print("The chat:",chat)
        temp = {'role':'user', 'content': open('prompts/narrator.txt','r').read() }
        temp['content'] += "The setting:\n" + open(self.setting, 'r').read()
        if(self.characters):
            temp['content'] += "\nAnd here are the player characters:\n" + "\n".join([open(character,'r').read() for character in self.characters['desc']])

        chat = [temp] + chat
        
        #print("the prepended chat:",chat)

        while(chat[-1]['role']==''):
            chat = chat[:-1]
        
        
        #print(chat)
        talking_over_chars=True
        i = 0

        temp_log=[] 
        while(talking_over_chars and i < 5):
            # TODO: change this to allow for tool calls. inventory editing, changing scene, getting info, etc.
            done=False
            temp_log=[]
            while( not done):
                done = True
                tool_calls=[]

                new_temp_log=[]
                for line in temp_log:
                    if type(line) == dict and (line['content']==None or not( len(line['content'])==0)):
                        new_temp_log.append(line)
                temp_log = new_temp_log
                
                #print(temp_log)

                if(self.model.startswith("gpt")):
                    response = self.client.chat.completions.create(
                            model = self.model,
                            messages = chat + temp_log,
                            tools =[ ast.literal_eval(open('prompts/gpt-narrator-tools.json','r').read())],
                            tool_choice = 'auto'
                            )
                    completion = response.choices[0].message.content
                    #temp_log.append(response.choices[0].message)
                elif(self.model.startswith("claude")):
                    response = self.client.messages.create(
                            model = self.model,
                            messages = chat + temp_log
                            )
                    completion = response.content.text
                    #temp_log.append(response)
               
#                print(response.choices[0])
                
                if self.model.startswith("gpt") and response.choices[0].finish_reason == 'tool_calls':
                   
                    #print(response.choices[0])
                    temp_log.append(dict(response.choices[0].message))
                    #print(response.choices[0].message)
                    #temp_log.append({'role':'assistant', 'content':completion})
                    tool_calls = response.choices[0].message.tool_calls
                    done=False

                elif self.model.startswith("claude") and response.stop_reason == 'tool_use':
                    temp_log.append({'role':'assistant', 'content':completion})
                    tool_calls = response.content
                    tool_content=[]
                    done=False
                
                
                for call in tool_calls:
                    tool_call_id = call.id
                    func_name = call.function.name if self.model.startswith("gpt") else call.name

                    arguments = ast.literal_eval(call.function.arguments) if self.model.startswith("gpt") else call.input

                    if(func_name=="lookup"):
                        print("Function call:",func_name, arguments)
                        #print(arguments)
                        result = toolcalls.RAG(arguments)         
                        #print("RESUTL:",result)


                    if(self.model.startswith("gpt")):
                        temp_log.append({'role':'tool', 'content':result, 'tool_call_id':tool_call_id, 'name':func_name, 'args':arguments})

                        #print(chat+temp_log)

                    elif(self.model.startswith("claude")):
                        tool_content.append({'type':'tool_result', 'tool_use_id': tool_call_id, 'content':result})
                if(self.model.startswith("claude")):
                    temp_log.append({'role':'user', 'content':tool_content})
                    
            i+=1



            completion = completion.replace("**","")
            talking_over_chars = any([name+":" in completion for name in self.characters['name']]) or any([name+" says" in completion for name in self.characters['name']])

        if(not completion.replace("**","").startswith("narrator:")):
            completion = "narrator:\n" + completion

        temp_log = temp_log[:-1]
        tool_results=[]
        for line in temp_log:
            if(line['role']=='tool'):
                tool_results += [
                    {
                        'role':'narrator\'s toolcall response',
                        'content':'result of '+line['name']+"("+str(line['args'])+"):\n"+line['content']
                    }]
    


        return  tool_results + [{"role":"narrator","content":completion}]





 
