from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.utils import timezone

from problembank.models import BankAccount
import datetime

JUST_VIEW_METHODS = ['GET']
JUST_ADD_METHODS = ['POST', 'GET']
EDIT_AND_DELET_METHODS = ['POST', 'GET', 'PUT', 'DELET']
SAFE_METHODS = ['POST', 'GET', 'PUT', 'DELET']
"""
POST = ADD NEW ONE
PUT = CHANGE
GET = READ
DELET = DELET
"""
class DefualtPermission(BasePermission):
    def has_anonymous_permission(self, request, view):
        return False 
        
    def has_member_permission(self, request, view):
        return False    
    
    def has_admin_prmission(self, request, view):
        return request.method in EDIT_AND_DELET_METHODS

    def has_permission(self, request, view):
        if request.user.is_anonymous :
            return self.has_anonymous_permission(request, view)
        elif request.user.account.position == BankAccount.Position.Member :
            return self.has_member_permission(request, view)
        elif request.user.account.position == BankAccount.Position.Admin:
            return self.has_admin_prmission(request, view)
        else :
            return False
