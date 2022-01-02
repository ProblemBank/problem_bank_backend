from django.db import transaction
from rest_framework import status

from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes


from problembank.models import ProblemGroup, Problem
from problembank.serializers import ProblemGroupSerializer

from rest_framework import permissions
from problembank.permissions import DefualtPermission, ProblemGroupPermission, AddProblemToGroupPermission

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
