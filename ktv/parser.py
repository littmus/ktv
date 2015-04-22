# -*- coding:utf8 -*-

import re

def strip_junk_tags(html):
    html = re.sub(r'/<head( |>)[\s\S]*?<\/head>/gi', '', html)
    html = re.sub(r'/<style( |>)[\s\S]*?<\/style>/gi', '', html)
    html = re.sub(r'/<script( |>)[\s\S]*?<\/script>/gi', '', html)
    html = re.sub(r'/<!--[\s\S]*?-->/gi', '', html)
    html = re.sub(r'/<\/style>/gi', '', html)

    return html

def get_error_msg(html):
    pass


