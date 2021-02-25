import tweetProcess
from utils import template
from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery("api", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(time_limit=300, soft_time_limit=240, bind=True)
def execute(self, src):
    src["template"] = template.TEMP[src["template_name"]]
    p = tweetProcess.Processor(src)
    file_name = p.process_tweet()
    return file_name
