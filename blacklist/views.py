from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin)
from .models import ListEntry
from .serializers import ListEntrySerializer


class ListEntryViewSet(GenericViewSet, CreateModelMixin,
                       RetrieveModelMixin, DestroyModelMixin):
    queryset = ListEntry.objects.all()
    serializer_class = ListEntrySerializer
    lookup_field = 'cpf'

    def retrieve(self, request, *args, **kwargs):
        status = ListEntry.STATUS_DENY

        filter_args = {self.lookup_field: kwargs.get('cpf')}
        try:
            ListEntry.objects.get(**filter_args)
        except ListEntry.DoesNotExist:
            status = ListEntry.STATUS_ALLOW

        return Response({'status': status})
