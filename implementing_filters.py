from bs4 import BeautifulSoup
from random import randint as rd
from requests import get, status_codes


# creating class

class WebCrawler:

    # constructor struct

    def __init__(self):

        # defining variables to scrap

        self.products_urls = []

        self.stars = 1

        self.keyword = ""

        self.min_price = int("0")

        self.max_price = int("0")

        self.until_page_num = 1

        self.sponsor_support = 0

        self.details_dictionary = []

        self.details_dictionary2 = []

        self.headers_identifier = 0

        # we'll randomize the headers in future

        self.headers_for_request = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          f'(KHTML, like Gecko) Chrome/1{rd(10,99)}.16{rd(0,9)}.9{rd(0,9)}.100 '
                          f'Safari/5{rd(0,99)}.{rd(0, 99)}',
            'Accept-Language': 'en-US, en;q=0.5',
            'Referer': 'https://www.amazon.com/',
            'Connection': 'keep-alive',
        }

        # running function in the beginning

        # get web content

    """gui tarafında sayfa numarası aprametresini bu fonksiyon alacak bu zaten otomatik olarak bağlı"""

    # updating_header

    def update_header(self):

        self.headers_for_request = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          f'(KHTML, like Gecko) Chrome/1{rd(10,99)}.16{rd(0,9)}.9{rd(0,9)}.100 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5',
            'Referer': 'https://www.amazon.com/',
            'Connection': 'keep-alive',
        }

    # requesting and parsing the web page

    def request_the_page_and_parse(self, page_num):
        """request and parsing function"""

        # request configurations

        self.searching_url = f"https://www.amazon.com/s?k={self.keyword}&rh=p_36%3A{self.min_price}00-" \
                             f"{self.max_price}00&ref=sr_pg_{page_num}"

        print(self.searching_url)

        # requesting url

        page_request = get(url=self.searching_url, headers=self.headers_for_request)

        # warn the user

        print(f"{page_request.status_code} is web response")

        # if bot detected

        if page_request.status_code == 503:

            self.update_header()

            self.request_the_page_and_parse(page_num)

        # going to feed beautiful soup with request

        # extract web contact from request

        web_content = BeautifulSoup(page_request.content, "lxml")

        return web_content

    # get products details from web content

    def details_of_products(self, html):

        # self.sponsor değişkeni değişecektirr
        # ürünlerin linkini de çıkartacağız

        # details of products div

        main_div = html.find_all("div", attrs={"class": "template=SEARCH_RESULTS"})

        # this section is tries to catch values
        # every product have name

        # catch sponsored product and filter it

        if self.sponsor_support == 0:

            # loop on all divs to turn into one div

            for name in main_div:

                # find name div and extract text

                product_name = name.find("div", attrs={"class": "s-title-instructions-style"}).text

                # catch sponsored text

                """unsponsored products section """

                if product_name.startswith("SponsoredSponsored"):

                    # if detected pass

                    pass

                # unsponsored products

                else:

                    # else try to get prices , don't forget every items may not have price

                    """getting price & stars try except blocks"""

                    try:

                        # price section

                        price_whole = name.find("span", attrs={"class": "a-price-whole"}).text

                        price_fraction = name.find("span", attrs={"class": "a-price-fraction"}).text

                        # links

                        link = name.find("a").get("href")

                        # election by stars and ratings

                        stars = name.find_all("span")

                        for star in stars:

                            # getting arie labels

                            star = star.get("aria-label")

                            # finding star pattern string in whole strings

                            if star is not None and "out of 5 stars" in star:

                                # get zeroth value to compare what we set the star

                                if int(star[0]) >= self.stars:
                                    # writing with tuple

                                    self.details_dictionary.append({"ürün adı": product_name,
                                                                    "ürün fiyatı": price_whole + price_fraction,
                                                                    "Yıldız": star[0:3],
                                                                    "Ürün linki": "https://www.amazon.com/" + link})

                    # if we couldn't get prices

                    except AttributeError:

                        price_fraction = 0

                        price_whole = 0

                        link = "Yok"

                        """print name, prices as a tuple"""

                        self.details_dictionary.append({"ürün adı": product_name,
                                                        "ürün fiyatı": price_whole + price_fraction,
                                                        "Yıldız": "Yok",
                                                        "Ürün linki": "https://www.amazon.com/" + link})

        else:

            """Sponsored products"""

            # it includes sponsored products

            print("--------------------SPONSORLU ÜRÜNLERİ İÇERİR-------------------------")

            for name in main_div:

                # find name div and extract text

                product_name = name.find("div", attrs={"class": "s-title-instructions-style"}).text

                """getting price & stars try except blocks"""

                try:

                    price_whole = name.find("span", attrs={"class": "a-price-whole"}).text

                    price_fraction = name.find("span", attrs={"class": "a-price-fraction"}).text

                    # links

                    link = name.find("a").get("href")

                    # finding stars and ratings div

                    stars = name.find_all("span")

                    for star in stars:

                        # getting arie labels

                        star = star.get("aria-label")

                        # finding star pattern string in whole strings

                        if star is not None and "out of 5 stars" in star:

                            # get zeroth value to compare what we set the star

                            if int(star[0]) >= self.stars:
                                # writing with tuple

                                self.details_dictionary.append({"ürün adı": product_name,
                                                                "ürün fiyatı": price_whole + price_fraction,
                                                                "Yıldız": star[0:3],
                                                                "Ürün linki": "https://www.amazon.com/" + link})

                    """print name, prices as a tuple"""

                # if we couldn't get prices

                except AttributeError:

                    price_fraction = 0

                    price_whole = 0

                    link = "Yok"

                    """print name, prices as a tuple"""

                    self.details_dictionary.append({"ürün adı": product_name,
                                                    "ürün fiyatı": price_whole + price_fraction,
                                                    "Yıldız": "Yok",
                                                    "Ürün linki": "https://www.amazon.com/" + link})

    # get shipping & rating & and many others from product's link

    # link is will be parameter this func derives from links of detail products

    def link_details_products(self, link_of_product):
        # randomize headers with identifier int

        self.headers_identifier += 1

        if self.headers_identifier == 20:
            print("--------HEADER UPTdated---------")
            self.headers_for_request = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              f'(KHTML, like Gecko) Chrome/1{rd(10, 99)}.16{rd(0, 9)}.9{rd(0, 9)}.100 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5',
                'Referer': 'https://www.amazon.com/',
                'Connection': 'keep-alive',
            }


        # requesting and parsing the links

        requesting = get(link_of_product, headers=self.headers_for_request)

        # if bot detected

        if requesting.status_code == 503:

            # update header

            self.update_header()

            self.link_details_products(link_of_product)

        # parse

        content_details_soup = BeautifulSoup(requesting.content, "lxml")

        try:

            # finding reviews and adding information to details list 2 we will merge with 1 after scraping

            # reviews filtre, canada işi ,

            # a lot of try excep conditions
            """1"""
            try:
                reviews = content_details_soup.find("span", attrs={"id": "acrCustomerReviewText"}).text
            except AttributeError:
                reviews = "Yok"
            """2"""
            try:
                shipping = content_details_soup.find("div", attrs={"id": "amazonGlobal_feature_div"}).text.split("&")[0]
            except AttributeError:
                shipping = "Yok"
            """3"""
            try:
                availability = content_details_soup.find("div", attrs={"id": "availability"}).text
            except AttributeError:
                availability = "yok"
            """4"""
            try:
                ship_from = content_details_soup.select("#tabular-buybox > div.tabular-buybox-container "
                                                        "> div:nth-child(4) > div > span")
                ship_from = [span.text for span in ship_from][0]
            except (AttributeError, IndexError):
                ship_from = "yok"
            """5"""
            try:
                sold_by = content_details_soup.select("#sellerProfileTriggerId")
                sold_by = [sold.text for sold in sold_by][0]
            except (AttributeError, IndexError):
                sold_by = "yok"
            # appending second dict

            self.details_dictionary2.append({
                "Görüntülünme": reviews,
                "Shipping ücreti": shipping,
                "Stock drumu": availability,
                "Gönderen": ship_from,
                "Tarafından Satılır": sold_by
            })

        except AttributeError:
            pass




