

import os, re

def RAG(regex, dirs): # goes through filenames in directories and append the content of the detected files.

    # I use a dict so later dirs overwrite earlier dirs. (for example, if setting changed how magic works, magic.txt in common would be replaced by magic.txt in the specific setting.)
    file_names=dict()
    regex.replace(" ","-") # invalidates some regex, but the ai is only using keyword searches right now.
    for i in range(len(dirs)):
        for path, subdirs, files in os.walk(dirs[i]):
            for name in files:
                if name.endswith(".txt") or name.endswith(".json"):
                    if(re.search(regex.lower(), name)): # invalidates some regex, but the ai is only using keyword seaarches right now.
                        file_names[name] = os.path.join(dirs[i], name)
    
    file_contents=[]

    size=0

    #print(file_names)

    for key in file_names:
        file_contents.append(open(file_names[key],'r').read() if key.endswith(".txt") else ast.literal_eval(open(file_names[key],'r').read())['desc'])
        size+=len(file_contents[-1])

    if(size / 5 >1000): # supposedly, a token is 5 characters on average.
        # sort files by number of regex hits. 
        file_contents.sort(key=lambda string: len(re.findall(regex, string)))
    
        # go down the list, adding a new file until you go over the limit.
        size=0
        i = 0
        new_file_contents=[]
        while(size/5<1000):
            new_file_contents.append(file_contents[i])
            size += len(file_contents[i])
            i+=1
        
        file_contents=new_file_contents


    ## pretty it up for the AI.
    file_contents = ("\n" + ("=" * 10) + "\n").join(file_contents)

    if(len(file_contents)==0):
        file_contents="File not found."

    return file_contents



#def 










