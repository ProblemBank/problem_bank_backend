from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from problembank.views import submitview as bank_submit_view
from Game2.permissions import IsAllowedTOPlay
from rest_condition import And
from Game2.models import Notification, Team, GameInfo
from problembank.models import Problem, BankAccount, JudgeableSubmit, ProblemGroup
from problembank.permissions import DefaultPermission
from Game2.utils import get_user_team


def send_notification(user, problem, mark, reward):
    data = {'title': "مسئله شما تصحیح شد."}
    mark = 'کامل' if mark == 1 else 'صفر'
    data['body'] = f"شما نمره {mark} را از  {problem.title} کسب کردید. {reward}  سکه به شما تعلق گرفت!"
    team = get_user_team(user)
    data['team'] = team
    data['time'] = timezone.now()
    Notification.objects.create(**data)


def get_problem_cost():
    return GameInfo.problem_cost


def get_users(user):
    team = get_user_team(user)
    return team.users.all()


def game_problem_request_handler(user, submit):
    problem_group = submit.problem_group
    team = get_user_team(user)
    if problem_group not in team.group_problems.all():
        for user in get_users(user):
            submit.respondents.add(user.account)
        submit.save()
        team = get_user_team(user)
        team.group_problems.add(problem_group)
        team.coin = team.coin - get_problem_cost()
        team.save()


def game_problem_request_permission_checker(gid, user):
    team = get_user_team(user)
    try:
        problem_group = ProblemGroup.objects.get(id=gid)
    except:
        problem_group = None
    if problem_group is None:
        return True
    elif problem_group in team.group_problems.all():
        return True
    if team.coin < GameInfo.problem_cost:
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
            if counter == GameInfo.max_not_submitted_problems:
                return True
    return False


def get_problem_reward(problem):
    if problem.difficulty == Problem.Difficulty.Easy:
        return GameInfo.easy_problem_reward
    elif problem.difficulty == Problem.Difficulty.Medium:
        return GameInfo.medium_problem_reward
    elif problem.difficulty == Problem.Difficulty.VeryHard:
        return GameInfo.so_hard_problem_reward
    else:
        return GameInfo.hard_problem_reward


def add_reward_to_team(team, problem):
    reward = get_problem_reward(problem)
    team.coin += reward
    team.save()
    return reward


def game_submit_handler(submit, user, problem):
    submit.status = JudgeableSubmit.Status.Delivered
    submit.save()
    team = Team.objects.filter(users__in=[user]).first()
    team.save()


def game_judge_handler(submit):
    reward = 0
    if submit.mark == 1:
        user = submit.respondents.all()[0].user
        team = get_user_team(user)
        problem = Problem.objects.filter(id=submit.problem.id)[0]
        reward = add_reward_to_team(team, problem)
        submit.status = JudgeableSubmit.Status.Judged
        submit.save()
    for account in submit.respondents.all():
        send_notification(account.user, submit.problem, submit.mark, reward)


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
    data = {'title': "مسئله شما تصحیح شد.", 'body': message, 'user': user, 'time': timezone.now()}
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


@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def judge_view(request, sid, mark):
    return bank_submit_view.judge_view(request.user.account, sid, mark, game_judge_handler)
