#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow, web


ICON_DEFAULT = 'icon.png'


# 加载
def data():
    url = 'https://raw.githubusercontent.com/Fyrd/caniuse/master/data.json'
    return web.get(url).json()

def main(wf):
    
    # 请求数据
    use_data = wf.cached_data('data', data, max_age=60 * 60 * 24)['data']
    # 添加 item 到 workflow 列表
    list = wf.filter(wf.args[0], use_data, key = lambda o: o)

    if not list:
        search_url = 'https://caniuse.com/#search=' + wf.args[0]
        wf.add_item('search on caniuse.com', arg = search_url)

    for key in list:
        url = 'https://caniuse.com/#feat=' + key
        val = use_data[key]
        wf.add_item(
            title = val['title'],
            subtitle = val['description'],
            arg = url,
            valid = True,
            icon = ICON_DEFAULT
        )

    wf.send_feedback()
    


if __name__ == '__main__':
    
    wf = Workflow()
    logger = wf.logger
    sys.exit(wf.run(main))
