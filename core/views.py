# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

from django.shortcuts import render, redirect
from accounts.forms import NewSnapLinkForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from SnapUp.settings import DEFAULT_FROM_EMAIL
from django.template import loader
from django.db.models import Q

from accounts.models import SnapLink, UserProfile

import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse
from twilio.rest import Client


from background_task import background

account_sid = "AC34e940b63fb3f17a65ca5522b176c35e"
auth_token = "49a00d9fa4785d133437c9999a9d9701"
client = Client(account_sid, auth_token)


def home(request):
    top_snapped_links = SnapLink.objects.filter(~Q(notify_me_type = 'None')).order_by('-date_added','-time_added','price')[:12]
    if request.method == 'POST':
        my_url_validator = URLValidator()
        my_url = request.POST.get("snap_link")
        try:
            my_url_validator(my_url)
            return scrape_snap_link(request, my_url)
        except ValidationError:
            messages.error(request, 'Oops!!!.....Please enter a valid link...')
            form = NewSnapLinkForm()
            return render(request, 'core/index.html', {'form': form, 'top_snapped_links': top_snapped_links})
    else:
        form = NewSnapLinkForm()
        return render(request, 'core/index.html', {'form': form, 'top_snapped_links': top_snapped_links})


@login_required
def scrape_snap_link(request, url):
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    req = urllib2.Request(url, headers=hdr)
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if domain == 'https://www.jumia.com.ng/':
        try:
            url_to_be_scraped = urllib2.urlopen(req)
            content = url_to_be_scraped.read()
            soup = BeautifulSoup(content, 'html.parser')
            title_box = soup.find('h1', attrs={'class': 'title'})
            price_box = soup.findAll('span', attrs={'class': 'price'})
            new_price_box = price_box[0]
            currency = new_price_box.find('span', attrs={'data-currency-iso': 'NGN'}).text
            price = new_price_box.find('span', attrs={'dir': 'ltr'}).text
            image_box = soup.findAll('img', attrs={'id': 'productImage'})
            for element in image_box:
                img_url = element['data-src']
            title = title_box.text.strip()
            img_url = img_url.strip()
        except urllib2.HTTPError, e:
            print e.fp.read()

        return render(request, 'core/snap_url_scraping.html', {'url': url, 'title': title, 'img_url': img_url, 'currency': currency, 'price': price})

    elif domain == 'https://www.konga.com/':
        try:
            url_to_be_scraped = urllib2.urlopen(req)
            content = url_to_be_scraped.read()
            soup = BeautifulSoup(content, 'html.parser')
            title_box = soup.find('div', attrs={'class': 'product-name'})
            price = soup.find('span', attrs={'class': 'price'}).text
            image_box = soup.findAll('img', attrs={'class': 'image-responsive'})
            for element in image_box:
                img_url = element['src']
            title = title_box.text.strip()
            currency = ''
        except urllib2.HTTPError, e:
            print e.fp.read()

        return render(request, 'core/snap_url_scraping.html', {'url': url, 'title': title, 'img_url': img_url, 'currency': currency, 'price': price})

    elif domain == 'https://jiji.ng/':
        try:
            url_to_be_scraped = urllib2.urlopen(req)
            content = url_to_be_scraped.read()
            soup = BeautifulSoup(content, 'html.parser')
            title_box = soup.find('h1', attrs={'class': 'b-advert__title h-mt-0 h-va-bottom pm-advert_name h-mv-0'})
            price = soup.findAll('div', attrs={'class': 'b-advert-seller__price pm-advert_price'})
            for element in price:
                price = element.span.text
            image_box = soup.findAll('ul', attrs={'data-bazooka': 'desktop-slider'})
            for element in image_box:
                img_url = element.li.img['src']
            title = title_box.text.strip()
            currency = ''
        except urllib2.HTTPError, e:
            print e.fp.read()

        return render(request, 'core/snap_url_scraping.html', {'url': url, 'title': title, 'img_url': img_url, 'currency': currency, 'price': price})

    elif domain == 'https://www.cheki.com.ng/':
        try:
            url_to_be_scraped = urllib2.urlopen(req)
            content = url_to_be_scraped.read()
            soup = BeautifulSoup(content, 'html.parser')
            title_box = soup.find('h1', attrs={'class': 'listing-detail__main-heading'})
            price = soup.findAll('div', attrs={'class': 'listing-detail__price-container'})
            for element in price:
                price = element.div.text
            image_box = soup.findAll('ul', attrs={'class': 'gallery__preview'})
            for element in image_box:
                img_url = element.li['data-src']
            title = title_box.text.strip()
            currency = ''
        except urllib2.HTTPError, e:
            print e.fp.read()

        return render(request, 'core/snap_url_scraping.html', {'url': url, 'title': title, 'img_url': img_url, 'currency': currency, 'price': price})

    elif domain == 'http://localhost:8000/':
        try:
            url_to_be_scraped = urllib2.urlopen(req)
            content = url_to_be_scraped.read()
            soup = BeautifulSoup(content, 'html.parser')
            title_box = soup.find('h2')
            price = soup.find('p').text
            image_box = soup.findAll('img')
            for element in image_box:
                img_url = 'http://localhost:8000'+ element['src']
            title = title_box.text.strip()
            currency = ''
        except urllib2.HTTPError, e:
            print e.fp.read()

        return render(request, 'core/snap_url_scraping.html', {'url': url, 'title': title, 'img_url': img_url, 'currency': currency, 'price': price})


def save_snap_link(request):
    url = request.POST.get("url")
    title = request.POST.get("title")
    img_url = request.POST.get("img_url")
    price = request.POST.get("price")
    currency = request.POST.get("currency")
    if SnapLink.objects.filter(user=request.user.username).filter(snap_link=url).exists():
        message = 'Oops!!!.....You\'ve already saved this Snap Link...'
        alert_class = 'alert-danger'
        return saved_snap_links(request, message, alert_class)
    else:
        SnapLink.objects.update_or_create(user=request.user.username, snap_link=url, title=title, img_url=img_url,price=price, currency=currency)
        message = 'Hurray!!!.....Your Snap link has been saved successfully, you can click on it to set up price notifications'
        alert_class = 'alert-success'
        return saved_snap_links(request, message, alert_class)


@login_required
def saved_snap_links(request, message, alert_class):
    snap_links = SnapLink.objects.filter(user=request.user.username).order_by('-date_added','-time_added')
    return render(request, 'core/my_snap_links.html', {'snap_links': snap_links, 'message': message, 'alert_class': alert_class})


@login_required
def my_snap_links(request):
    snap_links = SnapLink.objects.filter(user=request.user.username).order_by('-date_added','-time_added')
    return render(request, 'core/my_snap_links.html', {'snap_links': snap_links})


@login_required
def snap_link_details(request, id):
    snap_link = SnapLink.objects.get(pk=id)
    return render(request, 'core/snap_link_details.html', {'snap_link': snap_link})


@login_required
def notify_me_type(request, link_id, id):
    snap_link = SnapLink.objects.get(pk=link_id)
    SnapLink.objects.filter(pk=link_id).update(notify_me_type=id)
    if id == '1':
        message = 'there is a any change in the price...(basically to a lesser one)'
    elif id == '2':
        if 'percentage' in request.GET:
            percentage = request.GET['percentage']
            SnapLink.objects.filter(pk=link_id).update(percentage=percentage)
        message = 'price is decreased by your set percentage'
    elif id == '3':
        message = 'price is exactly equal to your set price...'
    messages.success(request, 'Congrats!!!.....You would be notified whenever ' + message)
    return render(request, 'core/snap_link_details.html', {'snap_link': snap_link})


@login_required
def check_price_change(request):
    all_links = SnapLink.objects.all()
    for link in all_links:
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        req = urllib2.Request(link.snap_link, headers=hdr)
        parsed_uri = urlparse(link.snap_link)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        if domain == 'http://localhost:8000/':
            try:
                url_to_be_scraped = urllib2.urlopen(req)
                content = url_to_be_scraped.read()
                soup = BeautifulSoup(content, 'html.parser')
                price = soup.find('p').text.replace(",", "").replace("₦", "")
                SnapLink.objects.filter(snap_link=link)
                if link.notify_me_type == '1':
                    link_price = link.price.replace(",", "").replace("₦", "")
                    user_account = User.objects.filter(username=link.user)
                    for user in user_account:
                        user_phone = user.userprofile.phone
                        if int(price) < int(link_price):
                            if user_phone != "":
                                user_phone = user_phone.lstrip("0")
                                user_phone = "+234"+user_phone
                                client.messages.create(to=user_phone,
                                                       from_="+15125984879",
                                                       body="Hello "+link.user.title()+ \
                                                            ", \nThere is a Lower Price Currently On the Shopping Website Of Your Snapped Link. \nVisit Now:"+unicode(link))
                            c = {
                                'email': user.email,
                                'domain': 'http://snapupng.pythonanywhere.com/',  # or your domain
                                'site_name': 'SnapUp',
                                'link': link,
                                'user': user,
                                'type': 'There is a Lower Price Currently On the Shopping Website',
                                'product_link': link.snap_link,
                                'protocol': 'http',
                            }
                            subject_template_name = 'core/price_notification.txt'
                            email_template_name = 'core/price_notification.html'
                            subject = loader.render_to_string(subject_template_name, c)
                            # Email subject *must not* contain newlines
                            subject = ''.join(subject.splitlines())
                            email = loader.render_to_string(email_template_name, c)
                            send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

                elif link.notify_me_type == '2':
                    link_price = link.price.replace(",", "").replace("₦", "")
                    percentage = link.percentage
                    percentage = int(percentage)/100
                    link_price = int(link_price) * percentage
                    user_account = User.objects.filter(username=link.user)
                    for user in user_account:
                        if int(price) == int(link_price):
                            if user_phone != "":
                                user_phone = user_phone.lstrip("0")
                                user_phone = "+234"+user_phone
                                client.messages.create(to=user_phone,
                                                       from_="+15125984879",
                                                       body="Hello "+link.user.title()+ \
                                                            ", \nPrice is Currently Equal To Your Percentage Drop On the Shopping Website Of Your Snapped Link. \nVisit Now:"+unicode(link))
                            c = {
                                'email': user.email,
                                'domain': 'http://snapupng.pythonanywhere.com/',  # or your domain
                                'site_name': 'SnapUp',
                                'link': link,
                                'user': user,
                                'type': 'Price is Currently Equal To Your Percentage Drop On the Shopping Website',
                                'product_link': link.snap_link,
                                'protocol': 'http',
                            }
                            subject_template_name = 'core/price_notification.txt'
                            email_template_name = 'core/price_notification.html'
                            subject = loader.render_to_string(subject_template_name, c)
                            # Email subject *must not* contain newlines
                            subject = ''.join(subject.splitlines())
                            email = loader.render_to_string(email_template_name, c)
                            send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

                elif link.notify_me_type == '3':
                    link_price = link.exact_price.replace(",", "").replace("₦", "")
                    user_account = User.objects.filter(username=link.user)
                    for user in user_account:
                        if int(price) == int(link_price):
                            if user_phone != "":
                                user_phone = user_phone.lstrip("0")
                                user_phone = "+234" + user_phone
                                client.messages.create(to=user_phone,
                                                       from_="+15125984879",
                                                       body="Hello " + link.user.title() + \
                                                            ", \nPrice is Exactly Equal To Your Set Price On the Shopping Website Of Your Snapped Link. \nVisit Now:" + unicode(
                                                           link))

                            c = {
                                'email': user.email,
                                'domain': 'http://snapupng.pythonanywhere.com/',  # or your domain
                                'site_name': 'SnapUp',
                                'link': link,
                                'user': user,
                                'type': 'Price is Exactly Equal To Your Set Price On the Shopping Website',
                                'product_link': link.snap_link,
                                'protocol': 'http',
                            }
                            subject_template_name = 'core/price_notification.txt'
                            email_template_name = 'core/price_notification.html'
                            subject = loader.render_to_string(subject_template_name, c)
                            # Email subject *must not* contain newlines
                            subject = ''.join(subject.splitlines())
                            email = loader.render_to_string(email_template_name, c)
                            send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

            except urllib2.HTTPError, e:
                print e.fp.read()



