import time
from tweetProcess import Processor
from utils import template
c = dict()
c = {
        "template_name": "akiba_temp",
        "link": "https://twitter.com/houshoumarine/status/1346429093319827456",
        "text": {
            "tweet": "新年🍑快乐🍑happy new🍑year",
            "retweet": "happy🍑new year🍑"
        },
        "type": "retweet"
}
#c['link'] = "https://twitter.com/omarupolka/status/1356459236075597824"
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