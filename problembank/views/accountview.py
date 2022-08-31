from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from problembank.models import *
from problembank.permissions import DefaultPermission
from problembank.serializers import BankAccountSerializer, PublicBankAccountSerializer


class AccountView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated, DefaultPermission]
    queryset = BankAccount.objects.all()

    def get_serializer_class(self):
        print(self.request.user)
        return BankAccountSerializer \
            if self.request.user.account.id == int(self.request.parser_context['kwargs'].get('pk', -1)) \
            else PublicBankAccountSerializer
