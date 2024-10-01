
import json, os

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

def jsonify(client, path, model):
    
    if(os.path.isfile(path.replace(".txt",".json"))):
        return open(path.replace(".txt",".json"),'r').read()


    if(model.startswith("gpt")):
        completion = client.chat.completions.create(
                model=model,
                messages = [{ "role": "user", "content": open("prompts/json_prompt.txt","r").read() + "\n" + open(path,'r').read()}],
                response_format = {"type":"json_object"}
                ).choices[0].message.content
        if(is_json(completion)):
            open(path.replace(".txt",".json"),'w').write(completion)
            return completion
        else:
            return None
    if(model.startswith("claude")):
        completion = client.messages.create(
                        model=model,
                        messages=[{
                            "role": 'user', "content":  open("prompts/character-to-json.txt",'r') + "\n" + open(path,'r').read()
                        }]
                      ).content[0].text
        # anthropic has no way to ensure their models will produce JSON. Here, I am stripping out any comments the model might have. 
        completion = re.sub("(^[\\s\\S]+?(?={))|([^}]+$)","",completion)
        if(is_json(completion)):
            open(path.replace(".txt",".json"),'w').write(completion)
            return completion
        else:
            return None
