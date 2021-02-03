import time
from tweetProcess import Processor
from utils import template
c = dict()
c = {
    "template_name": "akiba_temp",
    "link": "https://twitter.com/omarupolka/status/1356459236075597824",
    "text": {
        "tweet": ["新年快乐🍑1", "新年快乐🍑2"],
        "retweet": "happy new year🍑"
    },
    "type": "reply"
}
c['link'] = "https://twitter.com/omarupolka/status/1356459236075597824"
c["template"] = template.TEMP[c["template_name"]]
driver_init_time = time.time()
print("driver启动：" + str(driver_init_time))
p = Processor(c)
process_init_time = time.time()
print("process启动：" + str(process_init_time))
name = p.process_tweet()
process_ok_time = time.time()
print("process完成：" + str(process_ok_time))
print(f"driver启动耗时：{process_init_time - driver_init_time}")
print(f"process完成耗时：{process_ok_time - process_init_time}")