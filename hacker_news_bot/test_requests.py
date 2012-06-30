import urllib
import sys
from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(urllib.urlopen('http://news.ycombinator.com').read())
#print soup.prettify().encode('utf-8')

def wat():
    return lambda tag: tag.has_key('class')

def has_attr(attr_name, attr):
    return lambda tag: tag.has_key(attr_name) and tag[attr_name] == attr


stuff= soup.find_all(lambda tag: has_attr('class', ['title'])(tag) and has_attr('align', 'right')(tag))
#stuff= soup.find_all(lambda tag: has_attr('class', ['title'])(tag))
#stuff= soup.find_all(lambda tag: has_attr('align', 'right')(tag))
#stuff= soup.find_all(wat())

for tag in stuff:
    post = str(tag.parent) + str(tag.parent.next_sibling)
    print "post:"
#    print post
    post_soup = BeautifulSoup(post)
    for child in post_soup.children:
        
        print "child: " + str(child)
    sys.stdout.flush()

exit()

