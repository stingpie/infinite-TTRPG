



class arbiter():
    def __init__(self, characters, choose='round robin'):
        
        if(choose == "round robin"):
            self.choose = self.round_robin
            self.index = -1
        elif(choose == "random"):
            import random
            self.choose = random.choice
        elif(choose == "rand order"):
            import random
            self.index=-1
            self.choose = self.rand_choice
        elif(choose == "fair share"):
            import itertools, math
            self.choose = self.fair_share
            self.index=-1
        elif(choose == "rand fair share"):
            import random
            self.choose = self.rand_share_fair
            self.counts = [0] * len(characters)
        elif(choose == 'smart'): # this should scan the text for mentions of other characters, and trigger the most highly talked about character.
            
            import itertools, math
            self.iterations=0
            self.index=-1
            self.char_stack=[]
            self.choose=self.smart
        elif(type(choose) == 'method'):
            self.choose = choose

        self.narrators_turn=False
        
        self.characters = characters
        for character in self.characters:
            character.arbiter = self


    def round_robin(self):
        self.index = (self.index+1)%len(self.characters)
        return self.characters[self.index]

    def rand_order(self):
        if(self.index==0):
            random.shuffle(self.characters)
        self.index = (self.index+1)%len(self.characters)
        return self.characters[self.index]

    def fair_share(self):
        import math, itertools
        self.index = (self.index+1)%(math.factorial(len(self.characters)))
        z = list(itertools.permutations(self.characters))
        return z[self.index//len(self.characters)][self.index%len(self.characters)]
        
    def rand_fair_share(self):
        index=-1
        while(index==-1 or self.counts[index] == max(self.counts)):
            index = random.randint(0,len(self.characters))
        self.counts[index]+=1
        return self.characters[index]

    def smart(self):
        if(len(self.char_stack)==0):
            return self.fair_share()
        else:
            
            selected_char = self.char_stack[-1]
            self.char_stack.remove(selected_char)
            
            return selected_char

    def append_to_stack(self, character):
        if(self.choose != self.smart): ## error handling
            try:
                raise RuntimeError
            except Exception as e:
                e.add_note("Tried to append character to character stack, but arbiter is not set to 'smart' selection.")
                e.add_note("This is likely triggered by a model calling the 'speak_to' function, but not being stopped by the system.")
                raise
            
        for char in self.characters: # adding characters to the queue.
            if char.character_name == character or char.character_name.startswith(character):
                self.char_stack.append(char)
                return True
        self.narrators_turn=True
        return True

