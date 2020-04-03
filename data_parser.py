import pandas as pd
import xml.dom.minidom as minidom
import re
from bs4 import BeautifulSoup
from spellchecker import SpellChecker

spellchecker = SpellChecker(language="en", distance=1)

def remove_punctuation(raw_string):
    punctuation_re = r'[.,"\/#?!$%\^&\*;:{}=\-_`~()]'
    return re.sub(re.compile(punctuation_re), "", raw_string).lower()

def parse_posts(filename):
    filename = f"raw_data/{filename}.xml"
    raw_data = open(filename).read()
    posts_raw_strings = BeautifulSoup(raw_data, "xml").find_all("post")
    posts = [re.sub(r'</?post>', " ", str(s)).strip() for s in posts_raw_strings]
    posts = list(map(remove_punctuation, posts))
    words = parse_to_words(posts)
    print(words)

def check_words(formatted_words):
    checked = []
    for word in formatted_words:
        checked.append(spellchecker.correction(word))
    return checked

def parse_to_words(raw_posts):
    words = []
    counter = 0
    for post in raw_posts:
        post_words = post.split(" ")
        formatted_words = []
        skip_next = False
        for word in post_words:
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
        print(f"COUNTER: {counter}")
        counter += 1
    return words

parse_posts("1270648.female.23.indUnk.Scorpio")
