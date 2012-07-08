from bs4 import BeautifulSoup

class HNPost():
    '''
    Hacker News' html isn't organized ideally for this sort of thing.
    A "post" is made up of two consecutive <tr>'s. See HNPost.get_posts_html
    to see how those are obtained. This method creates a HNPost from
    those two rows
    '''
    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html)
        (title_row, info_row) = soup.children
        

    def __init__(self, title, url, id, comment_count, points, posted_ago, posted_by):
        '''
        keyword args:
        title - string
        url - url string
        id, comment_count, points - integer
        posted_ago, posted_by - string
        '''
        self.title = title
        self.url = url
        self.id = id
        self.comment_count = comment_count
        self.points = points
        self.posted_ago = posted_ago
        self.posted_by = posted_by

    

