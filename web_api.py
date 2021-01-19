from flask import Flask, request, jsonify, Response
import json
import socks
import socket
import os
import threading
import tweetProcess
from utils import template
from utils import qq_sender

socket.setdefaulttimeout(8)

app = Flask(__name__)


def handle_cook(src):
    src["template"] = template.TEMP[src["template_name"]]
    print(src)
    p = tweetProcess.Processor(src)
    name = p.process_tweet()
    file_path = os.getcwd() + '/imgs/' + name
    # print(file_path)
    if "QQ_bot" in src:
        qq_sender.push(src["QQ_bot"], name)
    return name


@app.route('/api/tweet_cook', methods=['POST'])
def get_task_result():
    data = request.data
    result = json.loads(str(data, encoding='utf-8'))
    if "type" in result:
        thd = threading.Thread(
            target=handle_cook,
            args=(result,)
        )
        thd.start()
        return Response(status=200)
    else:
        return Response(status=200)


if __name__ == "__main__":
    # a = {
    #     "proxy": "socks5://127.0.0.1:10808",
    #     "template_name": "akiba_temp",
    #     "link": "https://twitter.com/houshoumarine/status/1346429093319827456",
    #     "text": {
    #         "tweet": "新年🍑快乐🍑happy new🍑year",
    #         "retweet": "happy🍑new year🍑"
    #     },
    #     "type": "retweet"
    # }
    app.run(host="0.0.0.0", port=6001)
