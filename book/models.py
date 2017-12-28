# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



class Book(models.Model):
    asin = models.CharField(
        max_length=64,
        primary_key=True
    )
    isbn = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    author = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=256
    )
    publication_date = models.DateField()
    offer_url = models.URLField()
    large_image_url = models.URLField(
        null=True,
        blank=True
    )
    medium_image_url = models.URLField(
        null=True,
        blank=True
    )
    small_image_url = models.URLField(
        null=True,
        blank=True
    )
    product_group = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    sort_id = models.CharField(
        max_length=256,
    )

    def save(self, *args, **kwargs):
        self.sort_id = str(self.publication_date) + ":" + str(self.asin)
        return super(Book, self).save(*args, **kwargs)


    class Meta:
        ordering = ('-publication_date',)

    def __unicode__(self):
        string = self.title if self.title else u"タイトルなし"
        string += u" ("
        string += self.author if self.author else u"著者不明"
        string += u")"
        return string



class BookRelation(models.Model):
    title = models.CharField(
        max_length=256
    )
    original_title = models.CharField(
        max_length=256
    )
    translated_book = models.ForeignKey(
        Book,
        related_name="translated_book"
    )
    original_book = models.ForeignKey(
        Book,
        related_name="original_book",
        null=True,
        blank=True
    )
    publication_date = models.DateField()
    is_seen = models.BooleanField(
        default=False,
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    sort_id = models.CharField(
        max_length=256,
    )
    def save(self, *args, **kwargs):
        self.sort_id = str(self.publication_date) + ":" + str(self.translated_book.asin)
        return super(BookRelation, self).save(*args, **kwargs)
    class Meta:
        ordering = ('-publication_date',)


    def __unicode__(self):
        return unicode(self.translated_book)