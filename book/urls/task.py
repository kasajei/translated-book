from django.conf.urls import url

from book.tasks import FetchNewBooksTask, FetchProgressBooksTask, SaveAmazonTask

urlpatterns = [
    url(r"^fetch/new_books$", FetchNewBooksTask.as_view()),
    url(r"^fetch/progress_books$", FetchProgressBooksTask.as_view()),
    url(r"^save/amazon$", SaveAmazonTask.as_view()),
]
