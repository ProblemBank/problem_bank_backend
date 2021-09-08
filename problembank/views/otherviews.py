from rest_framework.response import Response
from problembank.models import Problem, ProblemGroup
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
def add_problem_to_group(request, pid, gid):
    try:
        problem = Problem.objects.filter(pk=pid)[0]
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        problem_group = ProblemGroup.objects.filter(pk=gid)[0]
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    problem_group.problems.add(problem)
    problem_group.save()

    return Response(f'مسئله {problem.pk} با موفقیت به گروه {problem_group.pk} اضافه شد.', status=status.HTTP_200_OK)


@api_view(['POST'])
def remove_problem_from_group(request, pid, gid):
    try:
        problem = Problem.objects.filter(pk=pid)[0]
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        problem_group = ProblemGroup.objects.filter(pk=gid)[0]
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    problem_group.problems.remove(problem)
    problem_group.save()

    return Response(f'مسئله {problem.pk} با موفقیت از گروه {problem_group.pk} حذف شد.', status=status.HTTP_200_OK)