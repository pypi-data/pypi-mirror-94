from djangoldp.views import LDPViewSet
from datetime import datetime
from .models import Event

class FutureEventsViewset(LDPViewSet):
    model = Event
    def get_queryset(self):
        return super().get_queryset().filter(startDate__gte=datetime.now())

class PastEventsViewset(LDPViewSet):
    model = Event
    def get_queryset(self):
        return super().get_queryset().filter(startDate__lt=datetime.now())
