import time
import urllib

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from scrapping.models import Category
from scrapping.models import Product


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


def get_from_jumia():
    # get all categories
    cats = Category.objects.all()
    for cat in cats:
        # html source
        opener = AppURLopener()
        html = opener.open("https://www.jumia.co.ke/%s/" % (cat.name,))
        # convert to soup
        soup = BeautifulSoup(html, "html.parser")
        # get all products
        products = soup.find_all("article", class_="prd _fb col c-prd")
        for product in products:
            # saving in the db
            try:
                url = (
                    "https://www.jumia.co.ke" + product.find("a", class_="core")["href"]
                )
                product_name = product.find("h3", class_="name").text
                raw_rating = product.find("div", class_="stars _s").text
                rating = float(raw_rating.split()[0]) if raw_rating else 0
                raw_price = product.find("div", class_="old").text
                raw_offer_price = product.find("div", class_="prc").text
                price = float(raw_price.split()[1]) if raw_price else 0
                offer_price = (
                    float(raw_offer_price.split()[1]) if raw_offer_price else 0
                )
                Product.objects.create(
                    url=url,
                    product_name=product_name,
                    price=price,
                    offer_price=offer_price,
                    rating=rating,
                    category_id=cat.id,
                )
                print("%s added succesfully" % (product_name,))
            except BaseException:
                print("%s error while adding" % (product_name,))


class Command(BaseCommand):
    help = "collect products"
    # define collect products logic command
    def handle(self, *args, **kwargs):

        """
        method to scrap data from kilimall
        """
        # initialize chrome webdriver
        driver = webdriver.Chrome("/home/tim/Downloads/chromedriver")
        driver.get("https://www.kilimall.co.ke/new/")
        search_items = [
            "shoes",
            "clothes",
            "electronics",
            "phones",
            "furniture",
            "music",
            "tvs",
            "alchohol",
            "fashion",
            "bags",
            "health",
            "food",
            "beauty",
        ]
        for search_item in search_items:
            # loop through all search items
            search = driver.find_element_by_class_name("el-input__inner")
            search.clear()
            search.send_keys(search_item)
            search.send_keys(Keys.ENTER)
            time.sleep(3)
            try:
                products = search.find_elements_by_xpath(
                    '//*[@id="__layout"]/section/main/div/div[2]/section/\
                        section/section/main/div/div/div[@class=\
                            "el-col el-col-6"]'
                )
            except TimeoutException:
                print("Timed out waiting for page to load")

            for product in products:
                # loop through all the product elements
                try:
                    link = product.find_element_by_tag_name("a")
                    url = link.get_attribute("href")
                    name = product.find_element_by_class_name("wordwrap").text
                    raw_offer_price = product.find_element_by_class_name(
                        "wordwrap-price"
                    ).text
                    raw_price = product.find_element_by_class_name("twoksh").text
                    offer_price = float(raw_offer_price.split()[1].replace(",", ""))
                    price = (
                        float(raw_price.split()[1].replace(",", "")) if raw_price else 0
                    )
                    raw_rating = product.find_element_by_xpath(
                        '//*[@id="__layout"]/section/main/div/div[2]/section/section/\
                            section/main/div/div/div[1]/div/div[2]/div/div[1]/\
                                div/div[@class="el-rate rateList"]'
                    )
                    rating = (
                        float(raw_rating.get_attribute("aria-valuenow"))
                        if raw_rating
                        else 0
                    )
                    pdt = Product(
                        url=url,
                        product_name=name,
                        price=price,
                        offer_price=offer_price,
                        rating=rating,
                    )
                    pdt.save()
                    print("%s added successfully" % (name,))
                except BaseException:
                    print("Error while adding")

        # quit browser session
        driver.quit()
        self.stdout.write("job completed")
