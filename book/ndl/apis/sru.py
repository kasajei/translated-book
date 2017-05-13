# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests
from pytz import UTC

from book.ndl.models import BookData


class SRU(object):
    URL = "https://iss.ndl.go.jp/api/sru"

    def __init__(self):
        """
        :param set: iss-ndl-opac, iss-ndl-opac-national, iss-ndl-opac-inprocess
        """
        self.operation = 'searchRetrieve'
        self.version = '1.2'
        self.startRecord = '1'
        self.maximumRecords = "200"
        self.startRecord = "1"
        self.recordPacking = 'string'
        self.recordSchema = 'dcndl_simple'
        self.inprocess = 'false'
        self.onlyBib = 'true'

        self.mediatype = "1"

    def __request(self, title=None, creator=None, isbn=None):
        query = {
            "operation": self.operation,
            "version": self.version,
            "startRecord": self.startRecord,
            "maximumRecords": self.maximumRecords,
            "recordPacking": self.recordPacking,
            "inprocess": self.inprocess,
            "recordSchema": self.recordSchema,
            "onlyBib": self.onlyBib,
        }
        query_string = "mediatype=" + self.mediatype
        if title:
            query_string += ' AND title="%s"' % title
        if creator:
            query_string += ' AND creator="%s"' % creator
        if isbn:
            query_string += ' AND isbn="%s"' % isbn

        query["query"] = query_string
        response = requests.get(self.URL, query)
        response.encoding = 'UTF-8'
        return response

    def __parse(self, xml):
        root = ElementTree.fromstring(xml.encode('utf-8'))
        records_root = root.find('{http://www.loc.gov/zing/srw/}records')
        books = []
        for record in records_root:
            recordData = record.find('{http://www.loc.gov/zing/srw/}recordData')
            item = recordData.find('{http://ndl.go.jp/dcndl/dcndl_simple/}dc')
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
    request = SRU()
    books = request.search(title=u"lean in")
    for book in books:
        print book.title
        print book.original_title
        print book.isbn
