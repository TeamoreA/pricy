from django.core.management.base import BaseCommand

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
from scrapping.models import  Product
from scrapping.models import  Category


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def get_from_killimall():
    # scrape killimall
    opener = AppURLopener()
    html = opener.open('https://www.kilimall.co.ke/new/commoditysearch?c=1057&aside=Phones%20%26%20Accessories&gc_id=1057')
    # convert to soup
    soup = BeautifulSoup(html, 'html.parser')
    import pdb; pdb.set_trace()
    # get all products
    products = soup.find_all("div", class_="grid-content bg-purple clearfix")
    for product in products:
        # saving in the db
        try:
            import pdb; pdb.set_trace()
            url = product.find('a', class_="link")['href']
            product_name = product.find('span', class_="name").text
            raw_rating = product.find('div', class_="total-ratings").text
            rating = int(raw_rating.replace('(', '').replace(')', '')) if raw_rating else 0
            raw_price = product.find('span', class_="price -old")
            raw_offer_price = product.find('span', class_="price")
            price = float(raw_price.getText().split('\n')[0].split()[1].replace(",", "")) if raw_price else 0
            offer_price = float(raw_offer_price.getText().split('\n')[0].split()[1].replace(",", "")) if raw_offer_price else 0
        Product.objects.create(
                url=url,
                product_name=product_name,
                price=price,
                offer_price=offer_price,
                rating=rating,
                category_id=cat.id
            )
            print('%s added succesfully' % (product_name,))
        except:
            print('%s error while adding' % (product_name,))

def get_from_jumia():
    # get all categories
    cats = Category.objects.all()
    for cat in cats:
        # html source
        opener = AppURLopener()
        html = opener.open('https://www.jumia.co.ke/%s/' % (cat.name,))
        # convert to soup
        soup = BeautifulSoup(html, 'html.parser')
        # get all products
        products = soup.find_all("div", class_="-gallery")
        for product in products:
            # saving in the db
            try:
                url = product.find('a', class_="link")['href']
                product_name = product.find('span', class_="name").text
                raw_rating = product.find('div', class_="total-ratings").text
                rating = int(raw_rating.replace('(', '').replace(')', '')) if raw_rating else 0
                raw_price = product.find('span', class_="price -old")
                raw_offer_price = product.find('span', class_="price")
                price = float(raw_price.getText().split('\n')[0].split()[1].replace(",", "")) if raw_price else 0
                offer_price = float(raw_offer_price.getText().split('\n')[0].split()[1].replace(",", "")) if raw_offer_price else 0
                Product.objects.create(
                    url=url,
                    product_name=product_name,
                    price=price,
                    offer_price=offer_price,
                    rating=rating,
                    category_id=cat.id
                )
                print('%s added succesfully' % (product_name,))
            except:
                print('%s error while adding' % (product_name,))



class Command(BaseCommand):
    help = "collect products"
    # define collect products logic command
    def handle(self, *args, **kwargs):
        # try:
        #     get_from_jumia()
        #     print('scrapping for jumia completed successfully')
        # except:
        #     pass
        try:
            get_from_killimall()
            print('scrapping for killimall completed successfully')
        except:
            pass

        # # get all categories
        # cats = Category.objects.all()
        # for cat in cats:
        #     # html source
        #     opener = AppURLopener()
        #     html = opener.open('https://www.jumia.co.ke/%s/' % (cat.name,))
        #     # convert to soup
        #     soup = BeautifulSoup(html, 'html.parser')
        #     # get all products
        #     products = soup.find_all("div", class_="-gallery")
        #     for product in products:
        #         # saving in the db
        #         try:
        #             url = product.find('a', class_="link")['href']
        #             product_name = product.find('span', class_="name").text
        #             raw_rating = product.find('div', class_="total-ratings").text
        #             rating = int(raw_rating.replace('(', '').replace(')', '')) if raw_rating else 0
        #             raw_price = product.find('span', class_="price -old")
        #             raw_offer_price = product.find('span', class_="price")
        #             price = float(raw_price.getText().split('\n')[0].split()[1].replace(",", "")) if raw_price else 0
        #             offer_price = float(raw_offer_price.getText().split('\n')[0].split()[1].replace(",", "")) if raw_offer_price else 0
        #             Product.objects.create(
        #                 url=url,
        #                 product_name=product_name,
        #                 price=price,
        #                 offer_price=offer_price,
        #                 rating=rating,
        #                 category_id=cat.id
        #             )
        #             print('%s added succesfully' % (product_name,))
        #         except:
        #             print('%s error while adding' % (product_name,))

        self.stdout.write( 'job completed' )