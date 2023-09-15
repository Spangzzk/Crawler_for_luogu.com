import unittest
from selenium import webdriver
from crawler import crawl

class CrawlerTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_crawl(self):
        difficulty = "入门"
        labels = ["o2", "递归"]
        num = 5

        crawl(difficulty, labels, num)

if __name__ == '__main__':
    unittest.main()