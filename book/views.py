# -*- coding: utf-8 -*-
import logging

import time
import urllib
import uuid
from urllib2 import HTTPError

from amazon.api import AmazonAPI
import re

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import requests_toolbelt.adapters.appengine
import unicodedata
from google.appengine.api.taskqueue import taskqueue

from book.models import BookRelation
from book.ndl.apis.opensearch import OpenSearch
from book.ndl.apis.sru import SRU
from book.serializers import BookRelationSerializer
from translated_book.settings import AMAZON_ACCESS_KEY, AMAZON_ACCOS_TAG
from translated_book.settings import AMAZON_ACCESS_SECRET

requests_toolbelt.adapters.appengine.monkeypatch()


class SearchView(APIView):
    def remove(self, books):
        translated_books = []
        for book in books:
            if book.original_title and book.author and book.isbn:
                translated_books.append(book)
        return translated_books

    def serialize(self, book):
        return {
            "title": book.title,
            "original_title": book.original_title,
            "author": book.author,
            "isbn": book.isbn
        }

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
        title = request.GET.get("title", None)
        isbn = request.GET.get("isbn", None)
        creator = request.GET.get("author", None)

        request = SRU()
        request.cnt = 20
        books = request.search(title, creator, isbn)
        books = self.remove(books)
        results = {
            "books": [self.serialize(book) for book in books]
        }
        for book in books:
            taskqueue.add(
                    url="/tasks/save/amazon",
                    params={
                        u"title": book.title,
                        u"original_title": book.original_title,
                        u"isbn": book.isbn
                    }
                )
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
                ids.append(product.isbn)
        return books


    def serialize_product(self, product):
        return {
            "asin": product.asin,
            "title": product.title,
            "isbn": product.isbn,
            "author": product.author,
            "publication_date": product.publication_date,
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
                -   name: isbn
                    type: string
                    paramType: query
        """
        title = request.GET.get("title", "")
        original_title = request.GET.get("original_title", "")
        isbn = request.GET.get("isbn", None)
        amazon = AmazonAPI(
            AMAZON_ACCESS_KEY,
            AMAZON_ACCESS_SECRET,
            AMAZON_ACCOS_TAG,
            region="JP",
            ErrorHandler=self.error_handler
        )
        if isbn:
            keyword = isbn
        else:
            keyword = u'"'+title+u'"|"'+original_title+u'"'

        try:
            logging.info(urllib.quote(keyword.encode("utf-8")))
        except:
            return Response()

        try:
            products = amazon.search_n(20, Keywords=keyword, SearchIndex=u'All')
        except UnicodeEncodeError:
            return Response({
                "isbn_prodcut": None,
                "translated_product": None,
                "original_product": None,
                "other_books":[]
            })
        products = self.remove(products)

        isbn_product = None
        if isbn:
            isbn_product = products[0]

        original_product = self.most_similarity_product(products, original_title, is_englsih=True)
        if original_product:
            products.remove(original_product)
        translated_product = self.most_similarity_product(products, title)
        if translated_product:
            products.remove(translated_product)

        results = {
            "isbn_product": self.serialize_product(isbn_product) if isbn_product else {},
            "translated_product": self.serialize_product(translated_product) if translated_product else {},
            "original_product": self.serialize_product(original_product) if original_product else {},
            "other_books": [self.serialize_product(product) for product in products]
        }
        return Response(results)


class RecentBookView(APIView):
    def get(self, request):
        """
        最新の翻訳本を取得する
        ---
        parameters:
                -   name: sort_id
                    type: string
                    paramType: query
                -   name: num
                    type: integer
                    paramType: query
        """
        page_size = int(request.GET.get("num", 25))
        queryset = BookRelation.objects
        if request.GET.get("sort_id"):
            queryset = queryset.filter(sort_id__lt=request.GET.get("sort_id"))

        queryset = queryset.prefetch_related(
            "translated_book"
        ).prefetch_related(
            "original_book"
        ).order_by("-sort_id")
        queryset = queryset[:page_size]
        queryset_json = BookRelationSerializer(
            queryset,
            many=True
        ).data
        last_sort_id = None
        logging.info(len(queryset_json))
        if len(queryset_json) == page_size:
            last_sort_id = queryset_json[-1]["sort_id"]
        resutls = {
            "last_sort_id": last_sort_id,
            "book_relations": queryset_json
        }
        return Response(resutls)