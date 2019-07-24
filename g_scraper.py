from bs4 import BeautifulSoup as bs
import requests
import xlsxwriter
from selenium import webdriver
#from selenium.webdriver.exceptions import NoSuchWebElementException
from selenium.webdriver.chrome.options import Options
import os


class Scraper():


    def __init__(self, num):
        self.row = 0
        self.workbook = xlsxwriter.Workbook("gledalica_filmovi.xlsx")
        self.worksheet = self.workbook.add_worksheet()
        print("Opening Driver")
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        self.pwd = os.getcwd()
        self.driver = webdriver.Chrome(executable_path=os.path.join(self.pwd, "chromedriver"), chrome_options=opt)


    def get_html(self, url):
        self.driver.get(url)
        h = self.driver.find_element_by_tag_name("body").get_attribute("innerHTML")
        print("Closing driver")
        #driver.close()
        return h

    def close_driver(self):
        self.driver.close()


    def request_page(self, html):
        soup = bs(html, "html.parser")
        movies = soup.select("li.video")
        print(f"Found {len(movies)}")
        if len(movies) > 0:
            print(f"Found {len(movies)} movies on this page")
            col = 0
            for movie in movies:
                title = movie.select("span.song_name")[0].text
                link = movie.select("a")[0]["href"]
                img = movie.select("img")[0]["src"]
                self.worksheet.write(self.row, col, title)
                self.worksheet.write(self.row, col+1, img)
                self.worksheet.write(self.row, col+2, link)
                self.row += 1
            return True
        else:
            return False

    def close_excel(self):
        self.workbook.close()


def main():
    num = 1
    s = Scraper(num)
    while True:
        url = f"https://www.gledalica.com/browse-HD-tablet-mobilni-videos-{num}-date.html"
        print(f"going to: {url}")
        html = s.get_html(url)
        stat = s.request_page(html)
        if stat == False:
            break
        num += 1
    s.close_excel()
    s.close_driver()
    print("FINISHED")


if __name__=="__main__":
    main()
