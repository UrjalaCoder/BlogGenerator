import pandas as pd
import xml.dom.minidom as minidom
import re
from bs4 import BeautifulSoup

# Illegal XML characters
RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                 u'|' + \
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                  (chr(0xd800),chr(0xdbff),chr(0xdc00),chr(0xdfff),
                   chr(0xd800),chr(0xdbff),chr(0xdc00),chr(0xdfff),
                   chr(0xd800),chr(0xdbff),chr(0xdc00),chr(0xdfff))

def load_xml(filename):
    filename = f"raw_data/{filename}.xml"
    raw_data = open(filename).read()
    soup = BeautifulSoup(raw_data).find_all("post")
    print(len(soup))

load_xml("1270648.female.23.indUnk.Scorpio")
