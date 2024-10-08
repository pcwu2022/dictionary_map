import json
import zipfile
import os

FOLDER_TO_ZIP = 'db'
OUTPUT_ZIP_FILE = 'db_vault.zip'
DATA_FILE = "data/word_adj_map_v1.json"

threshold = 150

def zip_folder(folder_path, output_zip):
    # Create a ZipFile object
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder and add each file to the zip
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to zip, preserving the folder structure
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


def load_dependencies():
    with open(DATA_FILE, "r") as file:
        word_adj_map = json.loads(file.read())
    return word_adj_map

def beautify(word):
    for character in ['/', '\\']:
        word = word.replace(character, ' ') # remove special characters and add space
    for character in ['\"', '.', ',', ';', ':', '~', '(', ')']:
        word = word.replace(character, '') # remove special characters
    word = word.replace('\'s', '') # remove 's
    word = word.lower()
    return word

def save_file(filename, context):
    with open(filename, 'w') as file:
        file.write(context)

def extract_json():
    word_adj_map = load_dependencies()
    i = 0
    for word in word_adj_map:
        if len(word_adj_map[word]) < threshold:
            continue
        md_context = '\n'.join(["[[" + w + "]]" for w in word_adj_map[word]])
        i += 1
        filename = FOLDER_TO_ZIP + "/" + beautify(word) + ".md"
        save_file(filename, md_context)
        
    print(f"Extracted {i} files with links > {threshold} to *.md")

extract_json()
zip_folder(FOLDER_TO_ZIP, OUTPUT_ZIP_FILE)