from django.core.management.base import BaseCommand

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from scrapping.models import  Product


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


class Command(BaseCommand):
    help = "collect products"

    # define collect products logic command
    def handle(self, *args, **kwargs):
        # html source
        opener = AppURLopener()
        html = opener.open('https://www.jumia.co.ke/phones-tablets/')

        # convert to soup
        soup = BeautifulSoup(html, 'html.parser')

        # get all products
        products = soup.find_all("div", class_="-gallery")
        import pdb; pdb.set_trace()
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
                    rating=rating
                )
                print('%s added succesfully' % (product_name,))
            except:
                print('%s error while adding' % (product_name,))

        self.stdout.write( 'job completed' )