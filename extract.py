import json
import zipfile
import os

folder_to_zip = './db'
output_zip_file = 'db_vault.zip'
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
    with open("word_adj_map.json", "r") as file:
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

def extract_json():
    word_adj_map = load_dependencies()
    for word in word_adj_map:
        md_context = '\n'.join(["[[" + w + "]]" for w in word_adj_map[word]])
        filename = "./db/" + beautify(word) + ".md"
        with open(filename, 'w') as file:
            file.write(md_context)

extract_json()
zip_folder(folder_to_zip, output_zip_file)