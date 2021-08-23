from rest_framework import permissions
from .models import *
from Game.models import *


class problem_sell_limit(permissions.BasePermission):
    
    def has_permission(self, request, view):
        seller = Player.objects.get(user=request.user)
        if Auction.objects.filter(player=seller, done_deal=False).count() > 10:
            return False
        
        else:
            return True


class seller_answer_problem(permissions.BasePermission):
    
    def has_permission(self, request, view):
        seller = Player.objects.get(user=request.user)
        problem = Problem.objects.get(id=request.data.get('problem_id'))
        
        if PlayerSingleProblem.objects.filter(player=seller, problem=problem, status='SCORED').exists() == True:
            return True
        else:
            return False


# , income__in=[1, 2]