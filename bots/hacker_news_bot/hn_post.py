import re
import urllib
import sys
from bs4 import BeautifulSoup

from bots.lib.util import get_logger, tag_has_attr

HACKER_NEWS_URL = 'http://news.ycombinator.com'
LOGGER = get_logger(__name__)

class HNPost():
    '''
    Notes:
        - HN one-indexes pages, I adhere to that.
    '''
    
    @classmethod
    def from_html(cls, html):
        '''
        Hacker News' html isn't organized ideally for this sort of thing.
        A "post" is made up of two consecutive <tr>'s. See HNPost.get_posts_html
        to see how those are obtained. This method creates a HNPost from
        those two rows.

        Also, since HN has recently thrown in sponsored links or something,
        this just doesn't work sometimes. For now if something goes wrong it
        is assumed that the post is atypical and just returns None.

        This is disgusting.
        '''
        try:
            soup = BeautifulSoup(html)
            (title_row, info_row) = soup.children
            #LOGGER.debug("title row: %s\ninfo row: %s", title_row, info_row)
            title_tag = title_row.find_all('a')[1]
            title = title_tag.text
            url = title_tag['href']
            comment_match = re.match('(?P<comment_count>\d+) comments?',
                                     info_row.find_all('a')[1].text)
            comment_count = 0
            if comment_match:
                comment_count = int(comment_match.group('comment_count'))
            id = int(re.match('score_(?P<id>\d+)', info_row.span['id']).group('id'))
            points = int(re.match('(?P<points>\d+) points?', info_row.span.text).group('points'))
            ago_groupdict = re.match('\s*(?P<amount>\d+) (?P<unit>.*) ago .*',
                                     info_row.find_all('a')[1].previous_element).groupdict()
            posted_ago = "%s %s" % (ago_groupdict['amount'], ago_groupdict['unit'])
            posted_by = info_row.find_all('a')[0].next_element
            return HNPost(title, url, id, comment_count, points, posted_ago, posted_by)
        except Exception as e:
            LOGGER.error("Something went wrong in parsing HN html: %s", e)
            return None

    def __init__(self, title, url, id, comment_count, points, posted_ago, posted_by):
        '''
        Keyword arguments:
        title -- string
        url -- url string
        id, comment_count, points -- integer
        posted_ago, posted_by -- string
        '''
        self.title = title
        self.url = url
        self.id = id
        self.comment_count = comment_count
        self.points = points
        self.posted_ago = posted_ago
        self.posted_by = posted_by

    @classmethod
    def get_posts_html(cls, page=1):
        '''
        Keyword arguments:
        page -- page number to pull from (default 1, the front page)

        Returns:
        List of html strings that each represent a post. From each element
        in this list a HNPost can be created using HNPost.from_html
        '''
        def is_title(tag):
            return tag_has_attr('class', ['title'])(tag) and tag_has_attr('align', 'right')(tag)

        url = cls.get_page_url(page)
        soup = BeautifulSoup(urllib.urlopen(url).read())
        titles = soup.find_all(is_title)
        # yeah.
        return map(lambda tag: str(tag.parent) + str(tag.parent.next_sibling),
                   titles)

    @classmethod
    def get_top_posts(cls, number=30, page=1):
        '''
        Keyword arguments:
        number -- number of posts desired (default 30, entire front page)
        page -- page number to start from (default 1, the front page)

        Returns:
        List of top <number> HNPost's
        '''
        return_me = []
        while len(return_me) < number:
            posts_html = cls.get_posts_html(page)
            for post in posts_html:
                hn_post = cls.from_html(post)
                if hn_post:
                    return_me.append(cls.from_html(post))
            page += 1
        return return_me[0:number]

    @classmethod
    def get_page_url(cls, page=1):
        '''
        Keyword arguments:
        page -- page number (>= 1) to fetch url for (default 1, the front page)
        
        Returns:
        URL of Hacker News page
        '''
        if page < 1:
            raise ValueError("Page number must be greater than 1. Given %d"
                             % (page))
        url = HACKER_NEWS_URL
        # Here's where shit gets bad. I don't know how HN generates
        # these page id's, but the only way to find them are using
        # the 'More' link at the bottom of the page before it
        if page > 1:
            # start at page 2
            url += '/news2'
            for page_num in range(3, page + 1):
                url = cls._get_more_url(url)
                #LOGGER.debug("HN page %d's url is %s", page_num, url)
        return url

    @staticmethod
    def _get_more_url(url):
        '''
        Argument:
        url -- HN url where the 'More' url will be found

        Returns:
        URL of the 'More' page from the given HN url
        '''
        soup = BeautifulSoup(urllib.urlopen(url).read())
        return HACKER_NEWS_URL + soup.find('a', text=re.compile('More'))['href']        

    def __unicode__(self):
        return "Post %s: %s" % (self.id, self.title)

    def __str__(self):
        return unicode(self).encode('utf-8')
