import json
import matplotlib.pyplot as plt
import math

DATA_FILE = "data/word_adj_map_v1.json"
OUTPUT_FILE = "data/word_adj_length.json"
OUTPUT_FIG = "data/word_length_calc.png"

word_adj_length = {}

def load_dependencies():
    with open(DATA_FILE, "r") as file:
        word_adj_map = json.loads(file.read())
    return word_adj_map

def save_output():
    with open(OUTPUT_FILE, "w") as file:
        file.write(json.dumps(word_adj_length, indent=4))

def plot_length():
    global word_adj_length
    max_word = max(word_adj_length, key=word_adj_length.get)
    max_length = word_adj_length[max_word]
    buckets = [0 for _ in range(int(math.log2(max_length)+1))]
    for word in word_adj_length:
        buckets[int(math.log2(word_adj_length[word]))] += 1
    plt.scatter(range(len(buckets)), buckets)
    plt.title("Number of Words - log(Word Appear Frequency)")
    plt.xlabel("log(Word Appear Frequency)")
    plt.ylabel("Number of Words")
    plt.savefig(OUTPUT_FIG)
    # plt.scatter(range(len(buckets)), [math.log2(x) for x in buckets])
    # plt.title("log(Number of Words) - log(Word Appear Frequency)")
    # plt.xlabel("log(Word Appear Frequency)")
    # plt.ylabel("log(Number of Words)")
    # plt.savefig(OUTPUT_FIG)
    

def extract_length():
    global word_adj_length
    word_adj_map = load_dependencies()
    del word_adj_map["current_parsing"]
    for key in word_adj_map:
        word_adj_length[key] = len(word_adj_map[key])
    word_adj_length = dict(sorted(word_adj_length.items(), key=lambda item: 0-item[1]))
    plot_length()
    save_output()

extract_length()