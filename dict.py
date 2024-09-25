import requests
import json

DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en"
word_adj_map = {}
current_parsing = "a"
word_list = []

def load_wordlist():
    global word_list
    with open("wordlist.txt", "r") as file:
        word_list = file.read().split('\n')

def load_dependencies():
    global current_parsing
    global word_adj_map
    with open("word_adj_map.json", "r") as file:
        word_adj_map = json.loads(file.read())
    current_parsing = word_adj_map["current_parsing"]

def dump_dependencies():
    global word_adj_map
    global current_parsing
    word_adj_map["current_parsing"] = current_parsing
    with open("word_adj_map.json", "w") as file:
        file.write(json.dumps(word_adj_map, indent=4, ensure_ascii=False))

def get_def(word):
    r = requests.get(DICT_API + "/" + word)
    j = json.loads(r.content)
    defs = []
    if type(j) != type(list()):
        return None
    for word in j:
        for meaning in word["meanings"]:
            for definition in meaning["definitions"]:
                defs.append(definition["definition"])
    return defs

def beautify(word_defs):
    word_def = ' '.join(word_defs) # list to string
    for character in ['/', '\\']:
        word_def = word_def.replace(character, ' ') # remove special characters and add space
    for character in ['\"', '.', ',', ';', ':', '~', '(', ')']:
        word_def = word_def.replace(character, '') # remove special characters
    word_def = word_def.replace('\'s', '') # remove 's
    word_def = word_def.lower()
    words_set = set(word_def.split(' '))
    word_defs = list(words_set)
    return word_defs

def find_dependencies(word):
    global word_adj_map
    word_defs = get_def(word)
    if word_defs == None:
        return
    word_defs = beautify(word_defs)
    for found in word_defs:
        if found in word_adj_map:
            if found not in word_adj_map[found]:
                word_adj_map[found].append(word)
        else:
            word_adj_map[found] = [word]

def generate_map(limit=100, step=10):
    global current_parsing
    load_wordlist()
    load_dependencies()
    start_index = word_list.index(current_parsing)
    for i in range(limit):
        find_dependencies(word_list[start_index + i])
        if i % step == step - 1:
            current_parsing = word_list[start_index + i + 1]
            print("Parsing: " + current_parsing)
            dump_dependencies()
            

# program execute
generate_map(100, 10)