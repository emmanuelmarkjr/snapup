# -*- coding: utf-8 -*-
from background_task import background
from datetime import timedelta
from django.shortcuts import render, redirect
from accounts.models import SnapLink

import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse


@background(schedule=5)
def timely_price_check(request):
    current_user_links = SnapLink.objects.filter(user=request.user.username).count()
    print (current_user_links)
    for link in current_user_links:
        link_to_chceck = SnapLink.objects.filter(snap_link=link)
        initial_price = link_to_chceck.price
        initial_price = initial_price.replace(",", "")
        initial_price = initial_price.replace("₦", "")
        notify_me_type = link_to_chceck.notify_me_type
        print(initial_price)
        print(notify_me_type)
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        req = urllib2.Request(link, headers=hdr)
        parsed_uri = urlparse(link)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        if domain == 'https://www.jumia.com.ng/':
            try:
                url_to_be_scraped = urllib2.urlopen(req)
                content = url_to_be_scraped.read()
                soup = BeautifulSoup(content, 'html.parser')
                price_box = soup.findAll('span', attrs={'class': 'price'})
                new_price_box = price_box[0]
                currency = new_price_box.find('span', attrs={'data-currency-iso': 'NGN'}).text
                # price = new_price_box.find('span', attrs={'dir': 'ltr'}).text
                price = '888000'
            except urllib2.HTTPError, e:
                print e.fp.read()
        if notify_me_type == '1':
            if price < initial_price:
                print ("this worked")
                return render(request, 'core/snap_url_scraping.html',
                              {'url': link, 'currency': currency, 'price': price})

        elif domain == 'https://www.konga.com/':
            try:
                url_to_be_scraped = urllib2.urlopen(req)
                content = url_to_be_scraped.read()
                soup = BeautifulSoup(content, 'html.parser')
                price = soup.find('span', attrs={'class': 'price'}).text
                currency = ''
            except urllib2.HTTPError, e:
                print e.fp.read()

            return render(request, 'core/snap_url_scraping.html',
                          {'url': link, 'currency': currency, 'price': price})

        elif domain == 'https://jiji.ng/':
            try:
                url_to_be_scraped = urllib2.urlopen(req)
                content = url_to_be_scraped.read()
                soup = BeautifulSoup(content, 'html.parser')
                price = soup.findAll('div', attrs={'class': 'b-advert-seller__price pm-advert_price'})
                for element in price:
                    price = element.span.text
                currency = ''
            except urllib2.HTTPError, e:
                print e.fp.read()

            return render(request, 'core/snap_url_scraping.html',
                          {'url': link, 'currency': currency, 'price': price})

        elif domain == 'https://www.cheki.com.ng/':
            try:
                url_to_be_scraped = urllib2.urlopen(req)
                content = url_to_be_scraped.read()
                soup = BeautifulSoup(content, 'html.parser')
                price = soup.findAll('div', attrs={'class': 'listing-detail__price-container'})
                for element in price:
                    price = element.div.text
                currency = ''
            except urllib2.HTTPError, e:
                print e.fp.read()

            return render(request, 'core/snap_url_scraping.html',
                          {'url': link, 'currency': currency, 'price': price})


