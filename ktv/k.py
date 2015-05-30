# -*- coding:utf8 -*-

import requests
from bs4 import BeautifulSoup as bs
import lxml

import parser

HOST = 'http://www.koreapas.com/m/'
LOGIN_URL = 'https://www.koreapas.com/bbs/login_check.php'
BOARD_URL = HOST + 'mlist.php'
VIEW_URL = HOST + 'view.php'
WRITE_URL = HOST + 'write.php'


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
        return bs(html, 'html5lib')

    def main(self):
        url = BOARD_URL
        params = {'id':'tiger'}
        r = self.get(BOARD_URL, params=params)
        soup = self.get_soup(r.content)
        options = soup.find('select').find_all('option')

        boards = []
        for option in options[7:]:
            boards.append((option.text, option['value'].split('=')[1]))

        return boards

    def board(self, board_id, page=1):
        url = BOARD_URL
        params = {'id': board_id, 'page': page}
        r = self.get(url, params=params)
        soup = self.get_soup(r.content)
        tables = soup.find_all('table')[1:]
        articles = filter(lambda l:l.get('bgcolor')=='#ffffff', tables)
        for article in articles:
            link = article.get('onclick')
            print link.split('=', 1)[1][1:-1]
            rows = article.find_all('tr')
            reply_count, title = [td.text.strip() for td in rows[0].find_all('td')]
            reply_count = 0 if reply_count == '' else reply_count
            print reply_count, title

            nick, timeago = [td.text.strip() for td in rows[1].find_all('td')]
            print nick, timeago

    def view(self, board_id, no):
        url = VIEW_URL
        params = {'id':board_id, 'no':no}
        return self.get(url, params=params)

    def write(self, board_id, mode='write'):
        url = WRITE_URL
        params = {'id': board_id, 'mode': mode}
        headers = {
            'Referer': BOARD_URL + '?id=%s' % board_id
        }
        return self.get(url, params=params, headers=headers)

    def comment(self):
        pass

if __name__ == '__main__':
    k = Koreapas()
    k.login('tedted', 'ted705')
    #k.main()
    #k.board('tiger')
    k.board('talk2')
    #print k.write('talk2').content.decode('euc-kr')
    #res = r.content
    #print res.decode('euc-kr')
