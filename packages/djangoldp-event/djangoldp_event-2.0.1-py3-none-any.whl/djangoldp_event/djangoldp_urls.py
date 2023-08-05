from django.conf.urls import url
from .views import FutureEventsViewset

urlpatterns = [
    url(r'^events/future/', FutureEventsViewset.urls(model_prefix="event-future"))
]

