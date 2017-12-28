# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from xml.etree import ElementTree

import requests
from pytz import UTC

from book.ndl.models import BookData


class OAIPMH(object):
    URL = "https://iss.ndl.go.jp/api/oaipmh"

    def __init__(self):
        """
        :param set: iss-ndl-opac, iss-ndl-opac-national, iss-ndl-opac-inprocess
        """
        self.verb = "ListRecords"
        self.metadata_prefix = "dcndl_simple"

        yesterday = datetime.now(UTC) - timedelta(days=1)
        self.from_date = yesterday.date()
        self.until_date = yesterday.date()
        self.set = "iss-ndl-opac"

        self.has_next = False

        self.__resumption_token = None


    def __request(self, resumption_token=None):
        query = {
            "verb": self.verb,
            "from": self.from_date,
            "until": self.until_date,
            "set": self.set,
            "metadataPrefix": self.metadata_prefix,
        }
        if resumption_token:
            query["resumptionToken"] = resumption_token
        response =  requests.get(self.URL, query)
        response.encoding = 'UTF-8'
        return response


    def __parse(self, xml):
        root = ElementTree.fromstring(xml.encode('utf-8'))
        list_records = root.find("{http://www.openarchives.org/OAI/2.0/}ListRecords")
        books = []
        if list_records is None:
            self.has_next = False
            self.__resumption_token = None
            return books
        for record in list_records:
            metadata = record.find("{http://www.openarchives.org/OAI/2.0/}metadata")
            if metadata is not None:
                book = BookData()
                rdf_root = metadata[0]
                title = rdf_root.find("{http://purl.org/dc/elements/1.1/}title")
                book.title = title.text.encode("utf-8") if title is not None else None
                author = rdf_root.find("{http://purl.org/dc/elements/1.1/}creator")
                book.author = author.text.encode("utf-8") if author is not None else None

                identifiers = rdf_root.findall("{http://purl.org/dc/elements/1.1/}identifier")
                for identifier in identifiers:
                    if identifier.get("{http://www.w3.org/2001/XMLSchema-instance}type") == u"dcndl:ISBN":
                        book.isbn = identifier.text.encode("utf-8")

                description = rdf_root.find("{http://purl.org/dc/terms/}description")
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
        resumption = list_records.find("{http://www.openarchives.org/OAI/2.0/}resumptionToken")
        if resumption is not None and resumption.text:
            self.__resumption_token = resumption.text.encode("utf-8")
            self.has_next = True
        else:
            self.__resumption_token = None
            self.has_next = False
        return books


    def load(self):
        response = self.__request()
        books = self.__parse(response.text)
        return books

    def load_next(self):
        response = self.__request(self.__resumption_token)
        books = self.__parse(response.text)
        return books

    def load_all(self):
        all_books = self.load()
        while self.has_next:
            all_books += self.load_next()
        return all_books


if __name__ == '__main__':
    request = OAIPMH()
    print(request.load())
    while request.has_next:
        print(request.load_next())

    books = request.load_all()
    for book in books:
        if book.original_title is not None:
            print book.title
            print(book.isbn, book.author, book.original_title)

    request.set = "iss-ndl-opac-inprocess"

    books = request.load_all()
    for book in books:
        print book.title
