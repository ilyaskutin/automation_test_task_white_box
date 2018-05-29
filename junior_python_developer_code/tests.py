import unittest
from check_urls_availability import check_urls
from check_urls_availability import NEEDED_URLS


class MyTests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(check_urls(NEEDED_URLS),
                         {k: v for k, v in zip(NEEDED_URLS, (True for _ in range(len(NEEDED_URLS))))})

    def test_2(self):
        urls = ('https://1233212312.com/', 'https://1ssa233212312.com/')
        self.assertEqual(check_urls(urls),
                         {k: v for k, v in zip(urls, (False for _ in range(len(urls))))})

    def test_3(self):
        my_cache = {}
        self.assertEqual(check_urls(NEEDED_URLS, my_cache),
                         {k: v for k, v in zip(NEEDED_URLS, (True for _ in range(len(NEEDED_URLS))))})
        self.assertEqual(check_urls(NEEDED_URLS, my_cache),
                         {k: v for k, v in zip(NEEDED_URLS, (True for _ in range(len(NEEDED_URLS))))})
        self.assertEqual(len(my_cache), 3)


if __name__ == '__main__':
    unittest.main()
