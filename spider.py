from urllib.request import urlopen
from link_finder import LinkFinder
from create_project import *
from domain import *
import os
import shutil

class Spider:
    # Class variables (shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    error_result_file =''
    queue = set()
    crawled = set()
    error = set()

    def __init__(self, project_name, base_url, domain_name, ):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.error_result_file = Spider.project_name + '/error.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_directory(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html; charset=utf-8' in response.getheader(
                    'Content-Type'):  # this might be evaluating the whole header
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print('Error: cannot crawl page: ' + page_url + '\n' + "Reason: " + str(e))
            error_result = 'Error: cannot crawl page: ' + page_url + '\n' + "Reason: " + str(e)
            Spider.error.add(error_result)
            Spider.update_files()
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        # for url in links:
        #     if url in Spider.queue:
        #         continue
        #     if url in Spider.crawled:
        #         continue
        #     if Spider.domain_name not in url:
        #         continue
        #     Spider.queue.add(url)
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        set_to_file(Spider.error,Spider.error_result_file)
