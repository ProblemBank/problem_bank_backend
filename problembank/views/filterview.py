from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from problembank.models import Problem
from problembank.serializers import FilterSerializer, ProblemSerializer
from problembank.permissions import ProblemPermission
from django.conf import settings
from problembank.serializers import FilterSerializer

def get_problems_by_filter(orderField=None ,topics=[], subtopics=[], \
                           sources=[],
                           grades=[], difficulties=[]):
    problems = Problem.objects.all()
    if len(topics) != 0:
        problems = problems.filter(topics__in=topics).distinct()

    if len(subtopics) != 0:
        problems = problems.filter(subtopics__in=subtopics).distinct()

    
    if len(sources) != 0:
        problems = problems.filter(source__in=sources)
   
    if len(grades) != 0:
        problems = problems.filter(grade__in=grades)

    if len(difficulties) != 0:
        problems = problems.filter(difficulty__in=difficulties)

    if orderField is not None:
        problems = problems.order_by(orderField)
    
    return problems.order_by('-id')


def get_problems_by_remove_permissions(request, problems):
    out_list = []
    qp = ProblemPermission()
    request.method = 'GET'
    for q in problems:
        request.parser_context['kwargs']['pk'] = q.pk
        if qp.has_permission(request, None):
            out_list.append(q)
    return out_list


@api_view(['POST'])
def get_problem_by_filter_view(request):
    serializer = FilterSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    data = serializer.validated_data
    page = data.pop("page")
    q_list = get_problems_by_filter(**data)
    paginator = Paginator(q_list, settings.CONSTANTS['PAGINATION_NUMBER'])
    page = paginator.get_page(page)
    problems_data = ProblemSerializer(page.object_list.select_subclasses(), many=True).data
    data = {'problems':problems_data,
            'pages_count':paginator.num_pages}
    return Response(data, status=status.HTTP_200_OK)