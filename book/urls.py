from django.conf.urls import url

from book.views import SearchView, AmazonView

urlpatterns = [
    url(r"^search/$", SearchView.as_view(), name="search"),
    url(r"^amazon/$", AmazonView.as_view(), name="amazon")
]
