# -*- coding:utf8 -*-
from __future__ import print_function, unicode_literals
import requests
from bs4 import BeautifulSoup as bs
import lxml

import parser

HOST = 'http://www.koreapas.com/m/'
LOGIN_URL = 'https://www.koreapas.com/bbs/login_check.php'
BOARD_URL = HOST + 'mlist.php'
VIEW_URL = HOST + 'view.php'
WRITE_URL = 'http://www.koreapas.com/bbs/write_ok.php'
COMMENT_URL = 'http://www.koreapas.com/bbs/vote_ex.php'

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
            if link is not None:
                link = link.split('=', 1)[1][1:-1]
            print(link)
            rows = article.find_all('tr')
            reply_count, title = [td.text.strip() for td in rows[0].find_all('td')]
            reply_count = 0 if reply_count == '' else reply_count
            print(reply_count, title)

            nick, timeago = [td.text.strip() for td in rows[1].find_all('td')]
            print(nick, timeago)

    def view(self, board_id, no):
        url = VIEW_URL
        params = {'id':board_id, 'no':no}
        return self.get(url, params=params)

    def write(self, board_id, subject, body):
        url = WRITE_URL
        params = {
            'mode': 'write',
            'id': board_id,
            'mobilemode': 'true',
            'use_html': '1',
            'subject': subject,
            'memo': body,
        }
        headers = {
            'Origin': 'http://www.kopreapas.com',
            'Referer': 'http://www.koreapas.com/bbs/write.php?id=%s&mode=write' % board_id,
            #'Referer': HOST + 'write.php?id=%s&mode=write' % board_id
        }

        return self.post(url, params=params, headers=headers)
        

    def comment(self, board_id, no, body, vote='ment', noname=1):
        url = COMMENT_URL
        params = {
            'id': board_id,
            'no': no,
            'ment_type': vote, # ment: 그냥, vote: 냉동
            'noname': noname, # 0 : 닉, 1 : 익명
            'memo': body
        }
        headers = {
            'Origin': 'http://www.koreapas.com',
#            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://www.koreapas.com/bbs/zboard.php?id=%s'
        }

        return self.post(url, params=params, headers=headers)


if __name__ == '__main__':
    k = Koreapas()
    k.login('tedted', 'ted705')
    #k.main()
    #k.board('tiger')
    #k.board('talk2')
    #res = k.write('talk2', 'asdf', 'asdf')
    res=k.comment('talk2', '3479326', u'가나다abc')
    print(res.content.decode('euckr'))
