from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes

from problembank.models import *
from rest_framework import permissions
# from problembank.views import permissions as customPermissions
from problembank.serializers import BankAccountSerializer, PublicBankAccountSerializer
from problembank.permissions import DefaultPermission
import sys

class AccountView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated, DefaultPermission]
    queryset = BankAccount.objects.all()

    def get_serializer_class(self):
        print(self.request.user)
        return BankAccountSerializer \
            if self.request.user.account.id == int(self.request.parser_context['kwargs'].get('pk', -1)) \
            else PublicBankAccountSerializer

# @api_view()
# def account_by_username(request):
#     try:
#         account = request.user.account
#     except:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
    
#     a_serializer = PrivateAccountSerializer(account)
#     return Response(a_serializer.data, status=status.HTTP_200_OK)
