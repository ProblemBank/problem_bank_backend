from django.db import transaction
from rest_framework import status

from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes


from problembank.models import ProblemGroup, Problem
from problembank.serializer import ProblemGroupSerializer, ProblemSerializer

from rest_framework import permissions
from problembank.permissions import DefaultPermission, ProblemGroupPermission, AddProblemToGroupPermission, CopyProblemToGroupPermission

class ProblemGroupView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    # permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission,]

    permission_classes = [permissions.IsAuthenticated, ProblemGroupPermission]
    queryset = ProblemGroup.objects.all()
    serializer_class = ProblemGroupSerializer    

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        data['problems'] = []
        serializer = ProblemGroupSerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            data['pk'] = request.data['pk']
        except:
            pass
        instance = serializer.create(data)
        instance.save()
       
        response = serializer.to_representation(instance)
        return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, AddProblemToGroupPermission])
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

@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, CopyProblemToGroupPermission])
def copy_problem_to_group(request, pid, gid):
    problem = Problem.objects.all().select_subclasses().filter(id=pid)[0]
    problem_group = ProblemGroup.objects.filter(id=gid)[0]
    problem_data = ProblemSerializer(problem).data
    problem_data['copied_from'] = problem.id
    problem_data['id'] = None
    problem_data['is_private'] = True
    problem_data['upvote_count'] = 0
    problem_data['is_checked'] = False
    problem_serializer = ProblemSerializer.get_serializer(problem.__class__)(data=problem_data)
    problem_serializer.is_valid()
    problem_data = problem_serializer.validated_data
    problem_data['author'] = request.user.account
    problem = problem_serializer.create(problem_data)
    problem_group.problems.add(problem)
    problem_group.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, AddProblemToGroupPermission])
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

