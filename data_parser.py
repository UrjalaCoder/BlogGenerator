import pandas as pd
import xml.dom.minidom as minidom
import re
from bs4 import BeautifulSoup

def remove_punctuation(raw_string):
    punctuation_re = r'[.,"\/#?!$%\^&\*;:{}=\-_`~()]'
    return re.sub(re.compile(punctuation_re), "", raw_string).lower()

def parse_posts(filename):
    filename = f"raw_data/{filename}.xml"
    raw_data = open(filename).read()
    posts_raw_strings = BeautifulSoup(raw_data, "xml").find_all("post")
    posts = [re.sub(r'</?post>', " ", str(s)).strip() for s in posts_raw_strings]
    posts = list(map(remove_punctuation, posts))
    print(posts[0:10])

parse_posts("1270648.female.23.indUnk.Scorpio")
