import tweetProcess
from utils import template as t
from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery("api", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
TEMPLATE = t.load_template()


@celery.task(time_limit=300, soft_time_limit=240, bind=True)
def execute(self, src: dict):
    if "template" not in src and "template_name" in src:
        # try to get template, if template is not exists then return default
        src["template"] = TEMPLATE.get(src["template_name"], TEMPLATE["default"])
    else:
        src["template"] = TEMPLATE["default"]
    p = tweetProcess.Processor(src)
    file_name = p.process_tweet()
    return file_name
