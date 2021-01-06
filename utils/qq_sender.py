import requests
import time
import os


def push_to_url(url):
    for retry in range(1, 4):
        status_code = 'fail'
        try:
            response = requests.post(url, timeout=10)
            status_code = response.status_code
        except:
            time.sleep(3)
        finally:
            print('[Info] pushtourl：第%s次-结果%s (%s)' % (retry, status_code, url))
            if status_code == 200:
                break


def push(src, name):
    # src = {
    #     "proxy": "socks5://127.0.0.1:10808",
    #     "template_name": "akiba_temp",
    #     "link": "https://twitter.com/houshoumarine/status/1346429093319827456",
    #     "text": {
    #         "tweet": "新年🍑快乐🍑happy new🍑year",
    #         "retweet": "happy🍑new year🍑"
    #     },
    #     "type": "retweet",
    #     "QQ_bot": {
    #         "url": "127.0.0.1",
    #         "port": "5701",
    #         "access_token": "",
    #         "group_id": "",
    #     }
    # }
    seen = "[CQ:image,file=file:///%s\\imgs\\%s.png]" % (os.getcwd(), name)
    url = f"http://{src['url']}:{src['port']}/send_group_msg?access_token={src['access_token']}&group_id={src['group_id']}&message={seen}"
    push_to_url(url)
