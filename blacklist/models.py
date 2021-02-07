from django.db import models
from .validators import validate_CPF


class ListEntry(models.Model):
    STATUS_ALLOW = "ALLOW"
    STATUS_DENY = "DENY"

    cpf = models.CharField(max_length=11, unique=True,
                           validators=[validate_CPF])

    def __str__(self):
        return self.cpf

    class Meta:
        verbose_name_plural = "list entries"
