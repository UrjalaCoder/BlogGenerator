import pandas as pd
import xml.dom.minidom as minidom
import re
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
import glob, os
import numpy as np

spellchecker = SpellChecker(language="en", distance=1)

def remove_punctuation(raw_string):
    punctuation_re = r'[.,"\/#?!$%\^&\*;:{}=\-_`~()]'
    return re.sub(re.compile(punctuation_re), "", raw_string).lower()

def parse_posts(filename, dictionary_dict):
    filename = f"raw_data/{filename}"
    raw_data = open(filename).read()
    posts_raw_strings = BeautifulSoup(raw_data, "xml").find_all("post")
    posts = [re.sub(r'</?post>', " ", str(s)).strip() for s in posts_raw_strings]
    posts = list(map(remove_punctuation, posts))
    posts = parse_to_words(posts)
    post_numericals = []
    for post in posts:
        post_number_list = []
        for word in post:
            index = None
            if word in dictionary_dict:
                index = dictionary_dict[word]
            else:
                index = len(dictionary_dict.keys())
                dictionary_dict[word] = index
            post_number_list.append(index)
        post_numericals.append(post_number_list)
    return post_numericals

def check_words(formatted_words):
    checked = []
    for word in formatted_words:
        checked.append(spellchecker.correction(word))
    return checked

def check_is_english(word):
    try:
        word.encode(encoding='utf-8').decode('ascii')
        return True
    except UnicodeDecodeError:
        return False
    else:
        return True

def parse_to_words(raw_posts):
    words = []
    counter = 0
    for post in raw_posts:
        skip_next = False
        post_words = post.split(" ")
        formatted_words = []
        for word in post_words:
            if check_is_english(word) is not True:
                break
            if word == "i":
                formatted_words.append("I")
            elif len(word) < 1:
                continue
            elif word == "urllink":
                skip_next = True
                continue
            elif skip_next is True:
                skip_next = False
                continue
            else:
                formatted_words.append(word)
        checked = check_words(formatted_words)
        words.append(checked)
        counter += 1
    return words

def save_post_data(numericals, dictionary_dict, filename="data"):


    numerical_array = []
    for blog in numericals:
        for post in blog:
            numerical_array.append(post)
    total_data = np.array([np.array(numerical_array), np.array(list(dictionary_dict.keys()))])
    try:
        np.save(f"parsed_data/{filename}", total_data)
        return True
    except Exception:
        print("FAILED TO SAVE")
        return False

def transform_to_string(post_list, dictionary_list):
    result_str_list = []
    for word_index in post_list:
         word = dictionary_list[word_index]
         result_str_list.append(word)
    return " ".join(result_str_list)

def load_post_data(filename="data"):
    data = np.load(f"parsed_data/{filename}.npy", allow_pickle=True)
    posts, keys = data
    return posts, keys

def parse_all():
    BASE_DATA_DIR = "./raw_data"
    dictionary_dict = {}
    post_numericals = []
    total_post_count = 0
    for f in glob.glob(f"{BASE_DATA_DIR}/*.xml"):
        if total_post_count > 10000:
            break
        b_name = os.path.basename(f)
        print(b_name)
        try:
            numericals = parse_posts(b_name, dictionary_dict)
            total_post_count += len(numericals)
            # print(numericals)
            print(f"POSTS: {total_post_count}")
            post_numericals.append(numericals)
        except UnicodeError:
            print(f"FAILED {b_name}")
            pass
    save_post_data(post_numericals, dictionary_dict)
