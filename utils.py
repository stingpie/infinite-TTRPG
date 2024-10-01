import ast, toolcalls










def history_to_chat(history, name, include_tool_calls=False):

    

    _history = copy(history)

    for i in range(len(_history)):
        if(_history[i]['role'] == name):
            _history[i]['role']="assistant"
        elif(include_tool_calls and _history[i]['role'] == name+"'s toolcall"):
            _history[i]['role']='assistant'
        elif(include_tool_calls and _history[i]['role']== name+"'s toolcall response"):
            _history[i]['role']='user'
        else:
            _history[i]['role']='user'
    

    new_hist=[]
    temp={'role':'', 'content':''}
    '''
    for i in range(len(_history)):
        if(temp['role']== 'assistant'):
            if(_history[i]['role']=='assistant'):
                temp['content'] += "\n" + _history[i]['content']
            else:
                new_hist.append(temp)
        elif(temp['role']== 'user'):
            if(_history[i]['role']=='user'):
                temp['content'] += "\n" + _history[i]['content']
            else:
                new_hist.append(temp)
        else:
            temp = _history[i]
        print(temp)
    new_hist.append(temp)
    '''

    if(len(_history)==0):
        _history=[{'role':'user','content':''}]





    return _history





def append_status(history, character):
    
    text = open("prompts/status.txt",'r').read()

    _history = copy(history)

    text = text.replace("${person_name}", character.name)
    text = text.replace("${character_name}", character.character_name)
    text = text.replace("${character_description}", character.description)
    text = text.replace("${chatacter_appearance}", character.appearance)
    text = text.replace("${chatacter_backstory}", character.backstory)
    text = text.replace("${character_personality}", character.personality)
    text = text.replace("${character_tags}", str(character.tags))
    text = text.replace("${character_inventory}", str(character.inventory))

    
    if(len(history)==1 and history[-1]['role']==''):
        if(character.model.startswith('gpt')):
            _history[-1]['role']='system'
        else:
            _history[-1]['role']='user'

    _history[-1]['content'] += "\n *** \n" + text + "\n *** \n"

    return _history

def prepend_character_info(history, character, setting, narrator=False):
   
    _history= copy(history)

    if(not narrator):
        text = open("prompts/AI-PC.txt",'r').read()

        setting = open(setting,'r').read()

        text = text.replace("${person_name}", character.name)
        text = text.replace("${character_name}", character.character_name)
        text = text.replace("${character_description}", character.description)
        text = text.replace("${chatacter_appearance}", character.appearance)
        text = text.replace("${chatacter_backstory}", character.backstory)
        text = text.replace("${character_personality}", character.personality)
    else:
        text = chracter.description


   
    
    
    if(len(history)==1 and _history[0]['role']==''):
        if(character.model.startswith('gpt')):
            _history[0]['role']='system'
        else:
            _history[0]['role']='user'

    _history[0]['content'] =  text + "\n *** \n" + setting + "\n***\n" + _history[0]['content']

    return _history

def complete_chat(client, model, chat, arbiter=None):
    

    if(chat[0]['role']==''):
        chat[0]['role']='user'
    
    temp_log=[]
    
    response=0
    done=False
    while( not done):
        done=True
        tool_calls=[]
        
        new_temp_log=[] # remove blank lines
        for line in temp_log:
            if(type(line) == dict and (line['content']==None or not (len(line['content'])==0))):
                new_temp_log.append(line)
        temp_log = new_temp_log

        if(model.startswith('gpt')):
            
            response = client.chat.completions.create(
                    model=model,
                    messages=chat + temp_log,
                    tools= [ast.literal_eval(open('prompts/gpt-character-tools.json','r').read())],
                    tool_choice='auto'
                    )
            
        else:
            
            response = client.messages.create(
                    model=model,
                    messages=chat + temp_log
                    )
        
        #print(response)
        
         
        if(model.startswith("gpt") and response.choices[0].finish_reason == 'tool_calls'):
            temp_log.append(dict(response.choices[0].message))
            tool_calls = response.choices[0].message.tool_calls
            done=False
        elif model.startswith("claude") and response.stop_reason == 'tool_use':
            temp_log.append({'role':'assistant','content':response.content.text})
            tool_calls = response.content
            tool_content=[]
            done=False

        for call in tool_calls:
            tool_call_id = call.id
            func_name = call.function.name if model.startswith("gpt") else call.name

            arguments = ast.literal_eval(call.function.arguments) if model.startswith("gpt") else call.input
            

            #print(func_name)
            if(func_name == "speak_to"):
                result = "Success." if toolcalls.stack(arbiter, arguments) else "Failed."


            if(model.startswith("gpt")):
                temp_log.append({'role':'tool', 'content': result, 'tool_call_id': tool_call_id, 'name':func_name})
            elif model.startswith("claude"):
                tool_content.append({'type':'tool_result', 'tool_use_id': tool_call_id, 'content':result})
        if(model.startswith("claude")):
            temp_log.append({'role':'user', 'content':tool_content})
    
    #output_text = response.choices[0].message.content if model.startswith("gpt") else response.content.text

    #if(re.search("^\s*(\S+\s*){1,4}:", output_text).group(0)[:-1] != 



    return response.choices[0].message.content if model.startswith("gpt") else response.content.text


def copy(array):
    new_array = []

    for i in array:
        new_array.append(i.copy())

    return new_array


