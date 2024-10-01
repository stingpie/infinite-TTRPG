import main, argparse, re

parser = argparse.ArgumentParser(description="infinite TTRPG.")
parser.add_argument('-c','--chars', type=str, nargs='+', help="list of character files you'd like a human or AI to play.")
parser.add_argument('-hc','--human-chars', type=str, nargs='+', help="list of character names you'd like a human to play.")
parser.add_argument('-n','--narrate', action='store_true', help='Whether a human plays as the narrator.')
parser.add_argument('-w','--world', type=str, default = 'lore/simple-setting', help='Directory of world lore.')
parser.add_argument('-r','--remind', action='store_true', help='Whether to remind characters of their current status.')
parser.add_argument('-m', '--model', type=str, default = 'gpt-4o-mini', help='What model to use (currently supports ChatGPT & Claude)')
#TODO: add options to choose arbitration type, and possible parallel chats.

args= parser.parse_args()

game = main.RPG(model = args.model, world = args.world, character_path = args.chars, remind_status = args.remind, human_characters=args.human_chars, player_narrator=args.narrate)


print("ready. type 'c' to continue.")
while(True):
    input_text = input("(TTRPG) ")
    if re.search("^\d+x", input_text):
        loops = int(input_text.split('x')[0])
        for i in range(loops):
            input_text = re.sub("^\d+x","", input_text)
            print(game.step( input_text.strip()))
            print()
    else:
        print(game.step(input_text.strip()))


