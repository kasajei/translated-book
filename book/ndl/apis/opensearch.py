# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests
from pytz import UTC

from book.ndl.models import BookData


class OpenSearch(object):
    URL = "https://iss.ndl.go.jp/api/opensearch"

    def __init__(self):
        """
        :param set: iss-ndl-opac, iss-ndl-opac-national, iss-ndl-opac-inprocess
        """
        self.mediatype = "1"
        self.cnt = "25"
        self.idx = "1"

    def __request(self, title=None, creator=None, isbn=None):
        query = {
            "title": title,
            "creator": creator,
            "isbn": isbn,
            "mediatype": self.mediatype,
            "cnt": self.cnt,
            "idx": self.idx,
        }

        response = requests.get(self.URL, query)
        response.encoding = 'UTF-8'
        return response


    def __parse(self, xml):
        root = ElementTree.fromstring(xml.encode('utf-8'))
        items = root.findall('.//item')
        books = []
        for item in items:
            book = BookData()
            title = item.find("{http://purl.org/dc/elements/1.1/}title")
            book.title = title.text.encode("utf-8") if title is not None else None
            author = item.find("{http://purl.org/dc/elements/1.1/}creator")
            book.author = author.text.encode("utf-8") if author is not None else None

            identifiers = item.findall("{http://purl.org/dc/elements/1.1/}identifier")
            for identifier in identifiers:
                if identifier.get("{http://www.w3.org/2001/XMLSchema-instance}type") == u"dcndl:ISBN":
                    book.isbn = identifier.text.encode("utf-8")

            description = item.find("{http://purl.org/dc/terms/}description")
            if description is not None and "原タイトル" in description.text.encode("utf-8"):
                original_title = ""
                for text in description.text.encode("utf-8").split():
                    match = re.match(r"[a-zA-Z0-9!-/-@¥[-`{-~]*", text)
                    if len(match.group()) > 1:
                        original_title += match.group() + " "
                original_title = original_title.rstrip()
                original_title = re.sub(r"[.:-@!]", "", original_title)
                book.original_title = original_title
            books.append(book)
        return books


    def search(self, title=None, creator=None, isbn=None):
        response = self.__request(title, creator, isbn)
        books = self.__parse(response.text)
        return books


if __name__ == '__main__':
    request = OpenSearch()
    books = request.search(u"SLEEP 最高の脳と身体をつくる睡眠の技術", u"ショーン")
    for book in books:
        print book.title
        print book.original_title
        print book.isbn