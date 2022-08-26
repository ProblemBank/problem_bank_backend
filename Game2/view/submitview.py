from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from problembank.views import submitview as bank_submit_view
from Game2.permissions import IsAllowedTOPlay
from rest_condition import And
from Game2.models import Notification, Team
from Game2.utils import get_user_team
from problembank.models import Problem, BankAccount, JudgeableSubmit
from problembank.permissions import DefaultPermission
from constants import PROBLEM_COST, EASY_PROBLEM_REWARD, MEDIUM_PROBLEM_REWARD, HARD_PROBLEM_REWARD,\
    MAX_NOT_SUBMITTED_PROBLEMS
from Game2.utils import get_user_team


def send_notification(team):
    data = {'title': "مسئله شما ارسال شد.", 'body': f"در حال نمره‌دهی به پاسخ شما هستیم", 'team': team,
            'time': timezone.now()}
    Notification.objects.create(**data)


def get_problem_cost():
    return PROBLEM_COST


def get_users(user):
    team = get_user_team(user)
    return team.users.all()


def game_problem_request_handler(user, submit):
    for user in get_users(user):
        submit.respondents.add(user.account)
    submit.save()

    team = get_user_team(user)
    team.coin = team.coin - get_problem_cost()
    team.save()


def game_problem_request_permission_checker(gid, user):
    team = get_user_team(user)
    if team.coin < PROBLEM_COST:
        return True
    return game_problem_request_first_handler(gid, user)


def game_problem_request_first_handler(gid, user):
    team = get_user_team(user)
    current_room = team.current_room
    groups = current_room.problem_groups.all()
    submits = JudgeableSubmit.objects.filter(
        problem_group__in=groups, respondents__in=[user.account])


    
    counter = 0
    for submit in submits:
        if submit.status == JudgeableSubmit.Status.Delivered:
            counter += 1
            if counter == MAX_NOT_SUBMITTED_PROBLEMS:
                return True
    return False


def get_problem_reward(problem):
    if problem.difficulty == Problem.Difficulty.Easy:
        return EASY_PROBLEM_REWARD
    elif problem.difficulty == Problem.Difficulty.Medium:
        return MEDIUM_PROBLEM_REWARD
    else:
        return HARD_PROBLEM_REWARD


def add_reward_to_team(user, submit, problem):
    team = get_user_team(user)
    team.coin += get_problem_reward(problem)
    team.save()


def game_submit_handler(submit, user, problem):
    submit.status = JudgeableSubmit.Status.Delivered
    submit.save()
    team = Team.objects.filter(users__in=[user]).first()
    send_notification(team)
    team.save()


@transaction.atomic
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAllowedTOPlay)])
def get_problem_from_group(request, gid):
    return bank_submit_view.request_problem_from_group_view(request.user.account, gid,
                                                            game_problem_request_handler,
                                                            game_problem_request_permission_checker)


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_problem_gotten_from_group(request, gid):
    return bank_submit_view.is_problem_gotten_from_group_view(request.user.account, gid)


@transaction.atomic
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAllowedTOPlay)])
def submit_answer(request, sid, pid):
    data = {
        'file': request.FILES['answerFile']
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
