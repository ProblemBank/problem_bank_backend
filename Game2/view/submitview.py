from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from problembank.views import submitview as bank_submit_view
from Game2.models import Team, Notification, TeamRoom, Room
from problembank.models import Problem, BankAccount
from problembank.permissions import DefaultPermission
from constants import PROBLEM_COST, EASY_PROBLEM_REWARD, MEDIUM_PROBLEM_REWARD, HARD_PROBLEM_REWARD


def send_notification(team, problem_group, mark):
    data = {
        'title': "مسئله شما تصحیح شد."
    }
    mark = 'کامل' if mark == 1 else 'صفر'
    data['body'] = f"شما نمره {mark} را از  {problem_group.title} کسب کردید."
    data['team'] = team
    data['time'] = timezone.now()
    Notification.objects.create(**data)


def get_problem_cost():
    return PROBLEM_COST


def get_users(user):
    team = Team.objects.filter(users__in=[user])[0]
    return team.users.all()


def game_problem_request_handler(user, submit):
    for user in get_users(user):
        submit.respondents.add(user.account)
    submit.save()

    team = Team.objects.filter(users__in=[user])[0]
    team.coin = team.coin - get_problem_cost()
    team.save()


def game_problem_request_permission_checker(gid, user):
    team = Team.objects.filter(users__in=[user])[0]
    if team.coin < PROBLEM_COST:
        return False
    return True


def get_problem_reward(problem):
    if problem.difficulty == Problem.Difficulty.Easy:
        return EASY_PROBLEM_REWARD
    elif problem.difficulty == Problem.Difficulty.Medium:
        return MEDIUM_PROBLEM_REWARD
    else:
        return HARD_PROBLEM_REWARD


def add_reward_to_team(user, submit, problem):
    team = Team.objects.filter(users__in=[user])[0]
    team.coin += get_problem_reward(problem)
    team.save()


def game_submit_handler(submit, user, problem):
    if submit.mark == 1:
        add_reward_to_team(user, submit, problem)
    submit.save()
    team = Team.objects.filter(users__in=[user])[0]
    send_notification(team, submit.problem_group, problem.mark)
    team.save()


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_problem_from_group(request, gid):
    return bank_submit_view.request_problem_from_group_view(request.user.account, gid,
                                                            game_problem_request_handler,
                                                            game_problem_request_permission_checker)


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_problem_gotten_from_group(request, gid):
    return bank_submit_view.is_problem_goten_from_group_view(request.user.account, gid)


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request, sid, pid):
    data = {
        'text': request.data['text'],
        'file': request.data['FILES']
    }
    return bank_submit_view.submit_answer_view(request.user.account, data, sid, pid, game_submit_handler)


def send_note(user, message):
    data = {}
    data['title'] = "مسئله شما تصحیح شد."
    data['body'] = message
    data['user'] = user
    data['time'] = timezone.now()
    Notification.objects.create(**data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, DefaultPermission])
def notification_to_all(request):
    for account in BankAccount.objects.all():
        try:
            send_note(account.user, message=request['message'])
        except:
            pass
    return Response(status=status.HTTP_200_OK)