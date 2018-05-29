# This code check what search service is available
# coding: utf-8

import requests
from multiprocessing import Pool as ThreadPool

NEEDED_URLS = ('https://google.com/', 'https://www.semrush.com/', 'https://yandex.ru/time/')
DEBUG = False


# Сделал отдельную функцию для загрузки ссылки
def load_url(url):
    try:
        content = requests.get(url).content
    except requests.exceptions.ConnectionError:
        content = ''
    return content


def check_urls(urls, cache=None):
    if cache is None:
        cache = {}
    result = {}
    urls_no_cache = []
    for url in urls:
        if url in cache:
            if DEBUG:
                print('url in cache ' + url)
            result.update({url: cache[url]})
        else:
            urls_no_cache.append(url)

    pool = ThreadPool(4)
    result.update({key: val for key, val in zip(urls_no_cache, pool.map(load_url, urls_no_cache))})
    pool.close()
    pool.join()
    cache.update(result)
    return {key: True if val != "" else False for key, val in result.items()}


if __name__ == '__main__':
    my_cache = {}
    print(check_urls(NEEDED_URLS, cache=my_cache))
    print(check_urls(NEEDED_URLS, cache=my_cache))
