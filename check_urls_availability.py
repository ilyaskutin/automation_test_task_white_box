
# This code check what search service is available
# coding: utf-8
NEEDED_URLS = ['https://google.com/', 'https://www.semrush.com/', 'https://yandex.ru/time/', 'https://yandex.ru/time/']

def get_fetch_urls(urls, cache={}):
    import requests
    urls_size = len(urls)
    result = []

    while urls_size:
        url = urls.pop()
        if url in cache:
            print('url in cache ' + url)
            result.append(cache[url])

        response = requests.get(url)
        body = response.content
        cache[url] = body
        result.append(body)
        urls_size -= 1

    return result
def get_full_moon_phase():
    import time
    time.sleep(5)
    import random
    time.sleep(5)
    return random.choice([True, False])

class UrlGetter:
    debug_mode_by_moon_phase = get_full_moon_phase()

    fetched_urls = []

    def __init__(self, fetched_urls):
        self.fetched_urls.extend(fetched_urls)

    def get_urls_data(self, urls):
        not_fetched_urls = []
        if self.debug_mode_by_moon_phase:
            for url in urls:
                print(url)
        for url in urls:
            if url not in self.fetched_urls:
                not_fetched_urls.append(url)
        data = get_fetch_urls(not_fetched_urls)
        self.fetched_urls.extend(not_fetched_urls)
        return data

    def check_url_not_fetched(self, url):
        if self.debug_mode_by_moon_phase:
            print(url in self.fetched_urls)
        return bool(url in self.fetched_urls)

# my tests

fetched_urls = ['https://google.com/']
getter = UrlGetter(fetched_urls)
for url in NEEDED_URLS:
    print(getter.check_url_not_fetched(url))
reuzuult1 = getter.get_urls_data(NEEDED_URLS)

import time
time.sleep(5)

fetched_urls = ['https://google.com/']
getter = UrlGetter(NEEDED_URLS)
reuzuult2 = getter.get_urls_data(NEEDED_URLS)


import os
file = open(os.getcwd()+'/data1.html', 'wb')
file.writelines(reuzuult1)
file2 = open(os.getcwd()+'/data2.html', 'wb')
file2.writelines(reuzuult2)

assert reuzuult1 == reuzuult2

if __name__ == '__main__':
    getter = UrlGetter()
    print(getter.get_urls_data(NEEDED_URLS))