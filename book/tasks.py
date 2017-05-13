# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import logging

from django.db import IntegrityError
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book, BookRelation
from book.ndl.apis.oaipmh import OAIPMH

from book.views import AmazonView
from google.appengine.api.taskqueue import taskqueue


class FetchNewBooksTask(APIView):
    def post(self, request):
        """
        新刊情報を取得する
        ---
        parameters:
                -   name: from_date
                    type: string
        """
        api = OAIPMH()
        logging.info(api.URL)
        from_date_string = request.POST.get("from_date", None)
        if from_date_string is not None:
            from_datetime = datetime.strptime(from_date_string, "%Y-%m-%d")
            api.from_date = from_datetime.date()
            api.until_date = (from_datetime + timedelta(days=1)).date()
        books = api.load_all()
        for book in books:
            if book.original_title is not None:
                taskqueue.add(
                    url="/tasks/save/amazon/",
                    params={
                        u"title": book.title,
                        u"original_title": book.original_title,
                        u"isbn": book.isbn
                    }
                )
        return Response({})


class FetchProgressBooksTask(APIView):
    def post(self, request):
        """
        新刊情報を取得する
        ---
        parameters:
                -   name: from_date
                    type: string
        """
        api = OAIPMH()
        api.set = "iss-ndl-opac-inprocess"
        from_date_string = request.POST.get("from_date", None)
        if from_date_string is not None:
            from_datetime = datetime.strptime(from_date_string, "%Y-%m-%d")
            api.from_date = from_datetime.date()
            api.until_date = (from_datetime + timedelta(days=1)).date()
        books = api.load_all()
        for book in books:
            if book.original_title is not None:
                taskqueue.add(
                    url="/tasks/save/amazon/",
                    params={
                        u"title": book.title,
                        u"original_title": book.original_title,
                        u"isbn": book.isbn
                    }
                )
        return Response({})


class SaveAmazonTask(APIView):
    def post(self, request):
        """
        新刊情報からAmazonを引っ張って保存する
        ---
        parameters:
                -   name: title
                    type: string
                -   name: original_title
                    type: string
                -   name: isbn
                    type: string
        """
        isbn = str(request.POST.get("isbn", ""))
        title = request.POST.get("title", "")
        original_title = request.POST.get("original_title", "")

        if Book.objects.filter(isbn=str(isbn)).exists():
            logging.info(title + u"はすでにあったよ!")
            return Response({})

        amazon = AmazonView()

        request.GET = {"original_title": original_title}
        response = amazon.get(request)
        data = response.data
        translated_book = None
        original_product = data["original_product"]
        original_book = None
        if original_product and original_product.get("asin", None) and original_product.get("publication_date", None):
            try:
                original_book, is_created = Book.objects.get_or_create(**original_product)
            except IntegrityError:
                pass


        request.GET = {"isbn": isbn}
        response = amazon.get(request)
        data = response.data
        translated_product = data["isbn_product"]
        translated_product["isbn"] = isbn
        if translated_product and translated_product.get("asin", None) and translated_product.get("publication_date", None):
            try:
                translated_book, is_created = Book.objects.get_or_create(**translated_product)
            except IntegrityError:
                pass

        if translated_book:
            book_relation, is_created = BookRelation.objects.get_or_create(
                title=title,
                original_title=original_title,
                publication_date=translated_book.publication_date,
                defaults={
                    "translated_book": translated_book,
                    "original_book": original_book,
                }
            )
        return Response(response.data)
