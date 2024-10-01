import tools

def RAG(args): ## Retrival augmented generation (A.K.A. GPT + googling)
    return tools.RAG(args['to_search'],['lore/common','lore/simple-setting'])

def stack(arbiter, args): ## push a character for future discussions
    if(arbiter.choose == arbiter.smart):
        return arbiter.append_to_stack(args['name'])
    return False


def add_tag(arbiter, args):
    for character in arbiter.characters:
        if character.character_name == args['name'] or character.character.startswith(args['name']):
            character.tags.append(args['tag'])
            return True
    return False


def remove_tag(arbiter, args):
    for character in arbiter.characters:
        if character.character_name == args['name'] or character.character.startswith(args['name']):
            try:
                character.tags.remove(args['tag'])
                return True
            except ValueError:
                return False

    return False



def add_item(arbiter, args):
    for character in arbiter.characters:
        if character.character_name == args['name'] or character.character.startswith(args['name']):
            character.inventory.append(args['item'])
            return True
    return False


def remove_item(arbiter, args):
    for character in arbiter.characters:
        if character.character_name == args['name'] or character.character.startswith(args['name']):
            try:
                character.inventory.remove(args['item'])
                return True
            except ValueError:
                return False
    return False

def get_tags(arbiter, args):
    for character in arbiter.characters:
        if character.character_name == args['name'] or character.character.startswith(args['name']):
            return character.tags
    return []

def get_inventory(arbiter, args):
    for character in arbiter.characters:
        if character.character_name == args['name'] or character.character.startswith(args['name']):
            return character.inventory
    return []




