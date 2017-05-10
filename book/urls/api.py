from django.conf.urls import url

from book.views import SearchView, AmazonView, RecentBookView

urlpatterns = [
    url(r"^search/$", SearchView.as_view(), name="search"),
    url(r"^amazon/$", AmazonView.as_view(), name="amazon"),
    url(r"^book/$", RecentBookView.as_view(), name="book"),
]
