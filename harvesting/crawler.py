'''
Created on Jan 7, 2013

@author: slarinier
'''
from selenium import webdriver
from pymongo import MongoClient
from threading import Thread
import redis
import threading
from pyfaup.faup import Faup
import time
from storage.redis_record import RedisRecord
from filters import Filters
from urllib2 import URLError
from collections import deque


class CrawlerThread(threading.Thread):
    def __init__(self, domain, db_value, lock):
        threading.Thread.__init__(self)
        self.domain = domain
        self.lock = lock

    def run(self):
        cw = Crawler(webdriver.Firefox(), self.lock, "http://" + self.domain)
        cw.init()
        cw.navigation()


class Record(threading.Thread):
    def __init__(self, db_value, lock):
        self.r = RedisRecord()
        self.connection = MongoClient(host='localhost', port=27017, db=db_value)
        self.db = self.connection[db_value]

        threading.Thread.__init__(self)
        self.lock = lock

    def run(self):
        i = 0
        while (True):
            i = i + 1
            if i % 1000 == 0:
                time.sleep(10)
            self.lock.acquire()
            self.r.switchDB(1)
            url = self.r.rpop('crawl')
            self.lock.release()
            # print url
            fex = Faup()
            if url:
                print "url found: " + url
                try:
                    fex.decode(url)
                    domain = fex.get_host()
                    entry = self.db.new_domaines.find_one({'domaine': domain})
                    if entry == None:
                        print "record: " + domain
                        self.db.new_domaines.save({'domaine': domain, 'urls': [url]})

                    urls_stored = entry['urls']
                    if not url in urls_stored:
                        urls_stored.append(url)
                        entry['urls'] = urls_stored
                        self.db.new_domaines.save(entry)
                except:
                    print "parsing fault " + url


class Crawler(object):
    def __init__(self, driver, lock, first_url, db_int=1):
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
        self.r = RedisRecord()
        self.lock = lock
        self.queue = deque([])
        self.queue.append(first_url)
        self.dbs = [1, 2]

    def init(self):
        self.r.init(self.dbs)
        url = self.queue.popleft()
        self.driver.get(url)
        self.parser(url)

    def parser(self, url):
        self.r.switchDB(1)
        if not self.r.get(url):
            self.driver.get(url)
            elem_links = self.driver.find_elements_by_tag_name('a')
            self.lock.acquire()
            self.sort([link.get_attribute("href") for link in elem_links], url)
            self.lock.release()
            self.r.switchDB(1)
            self.r.put(url, url)

    def navigation(self):

        while (len(self.queue) > 0):
            url = self.queue.popleft()
            try:
                # self.driver.refresh()
                self.r.switchDB(1)
                self.parser(url)

            except URLError as e:
                print url
            except IOError as e:
                self.r.switchDB(2)
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                # self.r.put(new_url,new_url)
                self.r.switchDB(1)
            except e:
                continue
        try:
            self.driver.quit()
            print "Fin du crawling du site " + url
        except URLError as e:
            self.driver = getattr(webdriver, 'Firefox')()
            print 'boum'
            self.lock.acquire()
            self.r.switchDB(1)
            self.r.put(url, url)
            self.lock.release()

    def sort(self, elem_links, url):
        fex = Faup()
        f = Filters()
        f.load()
        self.r.switchDB(1)
        extend = True
        domainfilter = True
        schemefilter = True
        try:
            for link in elem_links:
                new_url = link
                self.r.switchDB(2)
                if not self.r.get(new_url) and new_url:
                    self.r.switchDB(1)
                    if not self.r.get(new_url):
                        fex.decode(new_url)
                        domain = fex.get_host()
                        if f.isfilteredscheme(fex.get_scheme()):
                            self.r.switchDB(2)
                            self.r.put(new_url, new_url)
                            schemefilter = False
                        if f.isfiltereddomains(domain):
                            self.r.switchDB(2)
                            self.r.put(new_url, new_url)
                            domainfilter = False
                        if f.isfilteredextention(fex.get_resource_path()):
                            extend = False
                            self.r.switchDB(2)
                            self.r.put(new_url, new_url)

                        if extend and domainfilter and schemefilter:
                            self.r.switchDB(1)
                            self.r.rpush('crawl', new_url)
                            self.queue.append(new_url)
        except TypeError as e:
            print "TypeError"
