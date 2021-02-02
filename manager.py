import tweetProcess
from utils import template
from celery import Celery

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
celery = Celery("api", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(time_limit=300, soft_time_limit=240, bind=True)
def execute(self, src):
    src["template"] = template.TEMP[src["template_name"]]
    print(src)
    p = tweetProcess.Processor(src)
    file_name = p.process_tweet()
    return file_name
