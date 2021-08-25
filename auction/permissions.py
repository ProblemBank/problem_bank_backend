from rest_framework import permissions
from .models import *
from Game.models import *


class OpenAuctionsLimit(permissions.BasePermission):
    message = 'شما بیش از ۱۰ مزایده‌ی باز دارید.'

    def has_permission(self, request, view):
        game_id = request.data['game']
        seller = Player.objects.get(users__in=[request.user], game__id=game_id)
        if Auction.objects.filter(seller=seller, done_deal=False).count() > 10:
            return False
        else:
            return True


class DuplicateLimit(permissions.BasePermission):
    message = 'شما پیشتر این مسئله را به مزایده گذاشته‌اید.'

    def has_permission(self, request, view):
        game_id = request.data['game']
        problem_id = request.data['problem']
        seller = Player.objects.get(users__in=[request.user], game__id=game_id)
        problem = Problem.objects.get(id=problem_id)
        duplicate_auction = Auction.objects.filter(seller=seller, problem=problem).first()
        if duplicate_auction:
            return False
        else:
            return True


class SameSellerAndBuyer(permissions.BasePermission):
    message = 'شما نمی‌توانید سوالی را که خودتان به مزایده گذاشته‌اید، بخرید.'

    def has_permission(self, request, view):
        auction_id = request.data['auction']
        game_id = view.kwargs['game_id']
        auction = Auction.objects.get(id=auction_id)
        seller = Player.objects.get(users__in=[request.user], game__id=game_id)
        if auction.seller == seller:
            return False
        else:
            return True


class AlreadyHaveProblem(permissions.BasePermission):
    message = 'شما خودتان این مسئله را دارید!'

    def has_permission(self, request, view):
        auction_id = request.data['auction']
        game_id = view.kwargs['game_id']
        auction = Auction.objects.get(id=auction_id)
        player = Player.objects.get(users__in=[request.user], game__id=game_id)

        if Answer.objects.filter(player=player, problem__id=auction.problem.id).exists():
            return False
        else:
            return True


class seller_answer_problem(permissions.BasePermission):

    def has_permission(self, request, view):
        seller = Player.objects.get(user=request.user)
        problem = Problem.objects.get(id=request.data.get('problem_id'))

        if Answer.objects.filter(player=seller, problem=problem, status='SCORED').exists() == True:
            return True
        else:
            return False

# , income__in=[1, 2]
