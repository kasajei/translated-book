# -*- coding: utf-8 -*-
import logging

import time
import uuid
from urllib2 import HTTPError

from amazon.api import AmazonAPI
import re

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from pyndlsearch.client import SRUClient
from pyndlsearch.cql import CQL
import requests_toolbelt.adapters.appengine
import unicodedata

from translated_book.settings import AMAZON_ACCESS_KEY, AMAZON_ACCOS_TAG
from translated_book.settings import AMAZON_ACCESS_SECRET

requests_toolbelt.adapters.appengine.monkeypatch()


class SearchView(APIView):
    def get(self, request):
        """
        タイトルから
        ---
        parameters:
                -   name: title
                    type: string
                    paramType: query
                -   name: isbn
                    type: string
                    paramType: query
                -   name: author
                    type: string
                    paramType: query
        """
        title = request.GET.get("title", "")
        isbn = request.GET.get("isbn", "")
        creator = request.GET.get("author", "")

        cql = CQL()
        cql.title = title.encode("utf-8")
        cql.isbn = isbn.encode("utf-8")
        cql.creator = creator.encode("utf-8")
        cql.mediatype = u"1"  # 本のみ

        client = SRUClient(cql)
        client.set_only_bib(True)
        client.set_maximum_records(10)

        srres = client.get_srresponse()

        books = []
        titles = []
        for record in srres.records:
            if record.recordData.description and u'原タイトル' in record.recordData.description:
                original_title = ""
                for text in record.recordData.description.split():
                    match = re.match(r"[a-zA-Z0-9!-/-@¥[-`{-~]*", text)
                    if len(match.group()) > 1:
                        original_title += match.group() + " "
                original_title = original_title.rstrip()
                original_title = re.sub(r"[.:-@!]", "", original_title)
                if original_title not in titles:
                    titles.append(original_title)
                    book = {
                        "id": uuid.uuid4(),
                        "title": record.recordData.title,
                        "original_title": original_title,
                        "author": record.recordData.creator,
                    }
                    books.append(book)
        results = {
            "books": books
        }
        return Response(results)


class AmazonView(APIView):
    def error_handler(self, err):
        ex = err['exception']
        if isinstance(ex, HTTPError) and ex.code == 503:
            time.sleep(1)  # 1秒待つ
            return True

    def is_japanese(self, string):
        for ch in string:
            name = unicodedata.name(ch)
            if "CJK UNIFIED" in name \
            or "HIRAGANA" in name \
            or "KATAKANA" in name:
                return True
        return False

    def formatted_text(self, text):
        text = re.sub(r"[!-/:-@[-`{-~]", "", text)
        text = re.sub(re.compile(u"[︰ー＠―＆&「「」」]"), "", text)
        text = text.replace(u" ", u"")
        text = unicodedata.normalize(u"NFKC", text)
        return text.lower()

    def most_similarity_product(self, products, keyword, is_englsih=False):
        formated_keyword = self.formatted_text(keyword)
        for product in products:
            title = self.formatted_text(product.title)
            if (formated_keyword in title or title in formated_keyword) and u"Book" in product.get_attribute("ProductGroup") and product.author:
                if is_englsih:
                    if not self.is_japanese(title):
                        return product
                else:
                    return product
        if not is_englsih:
            for words in keyword.split(u":"):
                logging.info(words)
                for product in products:
                    title = self.formatted_text(product.title)
                    if self.formatted_text(words) in title and u"Book" in product.get_attribute("ProductGroup") and product.author:
                        if is_englsih:
                            if not self.is_japanese(title):
                                return product
                        else:
                            return product
        return


    def remove(self, products):
        books = []
        ids = []
        for product in products:
            product.id = product.asin
            if u"Book" in product.get_attribute("ProductGroup") and product.id not in ids:
                books.append(product)
                ids.append(product.id)
        return books


    def serialize_product(self, product):
        is_review, review_url = product.reviews
        return {
            "id": product.id,
            "asin": product.asin,
            "title": product.title,
            "isbn": product.isbn,
            "eisbn": product.eisbn,
            "author": product.author,
            "authors": product.authors,
            "review_url": review_url,
            "large_image_url": product.large_image_url,
            "small_image_url": product.small_image_url,
            "medium_image_url": product.medium_image_url,
            "offer_url": product.offer_url,
            "product_group": product.get_attribute("ProductGroup"),
        }

    def get(self, request):
        """
        タイトルからAmazon本を取得
        ---
        parameters:
                -   name: title
                    type: string
                    paramType: query
                -   name: original_title
                    type: string
                    paramType: query
        """
        title = request.GET.get("title", "")
        original_title = request.GET.get("original_title", "")
        amazon = AmazonAPI(
            AMAZON_ACCESS_KEY,
            AMAZON_ACCESS_SECRET,
            AMAZON_ACCOS_TAG,
            region="JP",
            ErrorHandler=self.error_handler
        )
        products = amazon.search_n(20, Keywords=u'"'+title+u'"|"'+original_title+u'"', SearchIndex='All')
        products = self.remove(products)
        original_product = self.most_similarity_product(products, original_title, is_englsih=True)
        if original_product:
            products.remove(original_product)
        translated_product = self.most_similarity_product(products, title)
        if translated_product:
            products.remove(translated_product)
        results = {
            "translated_product": self.serialize_product(translated_product) if translated_product else {},
            "original_product": self.serialize_product(original_product) if original_product else {},
            "other_books": [self.serialize_product(product) for product in products]
        }
        return Response(results)
