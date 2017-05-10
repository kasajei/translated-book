from django.contrib import admin

# Register your models here.
from book.models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date")

admin.site.register(Book, BookAdmin)



class BookRelationAdmin(admin.ModelAdmin):
    list_display = ("title", "original_title", "publication_date")

admin.site.register(BookRelation, BookRelationAdmin)