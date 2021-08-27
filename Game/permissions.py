from rest_framework import permissions
from .models import *
from Game.models import *


class ReceiveProblem(permissions.BasePermission):
    message = 'پیام خالی'

    def has_permission(self, request, view):
        if request.method == 'POST':
            user, difficulty, subject_id = request.user, request.data['difficulty'], request.data['subject']
            game_id = view.kwargs['game_id']
            player = Player.objects.get(game__id=game_id, users__in=[user])
            received_problems_count = Answer.objects.filter(player=player, status='RECEIVED').count()
            game = Game.objects.get(id=game_id)
            if received_problems_count >= game.maximum_number_of_received_problem:
                self.message = f'شما نمی‌توانید در یک لحظه بیش از {game.maximum_number_of_received_problem} مسئله‌ی دریافت‌شده داشته باشید.'
                return False

            player_problems = Answer.objects.filter(player=player).values_list('problem', flat=True)
            got_problems_from_specific_subject = player_problems.filter(problem__subject__id=subject_id)

            if got_problems_from_specific_subject.count() == game.maximum_number_of_received_problem_per_subject:
                self.message = f'شما نمی‌توانید بیش از {game.maximum_number_of_received_problem_per_subject} مسئله از این مبحث دریافت کنید.'
                return False

            available_problems = Problem.objects.filter(games__in=[game], difficulty=difficulty,
                                                        subject__id=subject_id) \
                .exclude(id__in=player_problems.all())
            if available_problems.count() == 0:
                self.message = 'شما تمام سوالات این بخش را گرفته‌اید!'
                return False

            return True
        return True

# class problem_sell_limit(permissions.BasePermission):
#     message = 'salam'
#
#     def has_permission(self, request, view):
#         seller = Player.objects.get(user=request.user)
#         if Auction.objects.filter(player=seller, done_deal=False).count() > 10:
#             return False
#
#         else:
#             return True


# class seller_answer_problem(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         seller = Player.objects.get(user=request.user)
#         problem = Problem.objects.get(id=request.data.get('problem_id'))
#
#         if Answer.objects.filter(player=seller, problem=problem, status='SCORED').exists() == True:
#             return True
#         else:
#             return False
#
# # , income__in=[1, 2]
