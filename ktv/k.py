# -*- coding:utf8 -*-

import requests
from bs4 import BeautifulSoup as bs

import parser

HOST = 'http://www.koreapas.com/m/'
LOGIN_URL = 'https://www.koreapas.com/bbs/login_check.php'
BOARD_URL = HOST + 'mlist.php?id=%s'
VIEW_URL = HOST + 'view.php?id=%s&no=%d'

class Koreapas(object):
    
    def __init__(self):
        self.session = requests.Session()

    def __del__(self):
        self.session.close()

    def login(self, _id, pw):
        data = {
            'user_id': _id,
            'password': pw,
            'x':0,'y':0,
        }
        r = self.post(LOGIN_URL, data=data)

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self.session.post(url, **kwargs)
    
    @staticmethod
    def get_soup(html):
        html = parser.strip_junk_tags(html)
        return bs(html)

    def main(self):
        r = self.get(BOARD_URL % 'tiger')
        soup = self.get_soup(r.content)
        selector = soup.find('select')

        boards = []
        for option in selector.find_all('option')[7:]:
            boards.append((option.text, option['value'].split('=')[1]))

        return boards

    def board(self, board_id):
        url = BOARD_URL % board_id
        r = self.get(url)
        soup = self.get_soup(r.content)
        
        articles = filter(lambda l:l.get('onclick') is not None, soup.find_all('table'))
        for article in articles[1:]:
            link = article.get('onclick')
            print link
            rows = article.find_all('tr')
            reply_count, title = [td.text.strip() for td in rows[0].find_all('td')]
            print reply_count, title

            nick, timeago = [td.text.strip() for td in rows[1].find_all('td')]
            print nick, timeago

    def view(self, board_id, no):
        url = VIEW_URL % (board_id, no)
        return self.get(url)

if __name__ == '__main__':
    k = Koreapas()
    k.login('ehddnjsdld', 'ted705')
    print k.main()
    k.board('tiger')
    #r = k.view('talk2', 3446655)
    #res = r.content
    #print res.decode('euc-kr')
