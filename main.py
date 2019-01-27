import threading
from queue import Queue
from spider import Spider
from domain import *
from create_project import *

PROJECT_NAME = 'bsdsitecrawler'
BASE_URL = 'https://main-staging2.bsd.net/j/step/fdgtrghrsfdgbdsfhdfg'
DOMAIN_NAME = get_domain_name(BASE_URL)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, BASE_URL, DOMAIN_NAME)


# Create worker threads (will be killed when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link will be new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue.')
        create_jobs()


create_workers()
crawl()
