# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from pyndlsearch.client import SRUClient
from pyndlsearch.cql import CQL
import requests_toolbelt.adapters.appengine
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
        cql.fromdate = u'2000-10-10'

        client = SRUClient(cql)
        client.set_only_bib(True)
        client.set_maximum_records(10)

        srres = client.get_srresponse()

        books = []
        for record in srres.records:
            if record.recordData.description and u'原タイトル: ' in record.recordData.description:
                original_title = record.recordData.description.replace(u"原タイトル: ", "")
                book = {
                    "title": record.recordData.title,
                    "original_title": original_title,
                    "author": record.recordData.creator,
                }
                books.append(book)
        results = {
            "books": books
        }
        return Response(results)