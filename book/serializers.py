# -*- coding: utf-8 -*-
from rest_framework import serializers

from book.models import Book, BookRelation


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "asin",
            "title",
            "offer_url",
            "large_image_url",
            "medium_image_url",
            "small_image_url",
            "author",
            "publication_date",
        )


class BookRelationSerializer(serializers.ModelSerializer):
    translated_book = BookSerializer()
    original_book = BookSerializer()


    class Meta:
        model = BookRelation
        fields = (
            "title",
            "original_title",
            "translated_book",
            "original_book",
            "publication_date",
            "sort_id",
        )