from django.forms import ValidationError
from rest_framework import exceptions
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin)
from .models import ListEntry
from .serializers import ListEntrySerializer
from .validators import validate_CPF


class ListEntryViewSet(GenericViewSet, CreateModelMixin,
                       RetrieveModelMixin, DestroyModelMixin):
    queryset = ListEntry.objects.all()
    serializer_class = ListEntrySerializer
    lookup_field = 'cpf'

    def retrieve(self, request, *args, **kwargs):
        cpf = kwargs.get('cpf')
        try:
            validate_CPF(cpf)
        except ValidationError as e:
            raise exceptions.ValidationError({"detail": ",".join(e)})

        status = ListEntry.STATUS_DENY

        filter_args = {self.lookup_field: cpf}
        try:
            ListEntry.objects.get(**filter_args)
        except ListEntry.DoesNotExist:
            status = ListEntry.STATUS_ALLOW

        return Response({'status': status})
