import logging

from config.celery import app


logger = logging.getLogger(__name__)


@app.task(bind=True)
def update_rss_feeds(self, *args, **kwargs):
    print("executing...")
