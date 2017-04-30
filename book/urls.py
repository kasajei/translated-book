from django.conf.urls import url

from book.views import SearchView

urlpatterns = [
    url(r"^search/$", SearchView.as_view(), name="search")
]
