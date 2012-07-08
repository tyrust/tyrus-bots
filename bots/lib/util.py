'''
util.py
A set of utility methods that may be utilitzed by all bots at some point.
'''

from bs4 import BeautifulSoup

# BeautifulSoup functions

def tag_has_attr(attr_name, attr):
    '''
    Keyword arguements:
    attr_name -- desired attribute
    value -- desired value of attribute
    
    Returns a function that takes a tag. This function determines if
    the tag has the attribute attr_name with the value value.

    Usage example to find all tags with align='right' in soup:
    soup.find_all(tag_has_attr('align', 'right'))    
    '''
    return lambda tag: tag.has_key(attr_name) and tag[attr_name] == attr
