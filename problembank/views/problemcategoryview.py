from django.db import transaction
from rest_framework import status

from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import mixins


from problembank.models import ProblemCategory
from problembank.serializers import ProblemCategorySerializer, ProblemCategoryGetSerializer

from rest_framework import permissions


class ProblemCategoryView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.UpdateModelMixin):
    # permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission,]

    queryset = ProblemCategory.objects.all()
    serializer_class = ProblemCategorySerializer

    def get_serializer_class(self):
        return ProblemCategoryGetSerializer \
            if self.request.method == 'GET' \
            else ProblemCategorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        data['problems'] = []
        serializer = ProblemCategorySerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        try:
            data['pk'] = request.data['pk']
        except:
            pass
        instance = serializer.create(data)
        instance.save()
        # if 'widgets' in request.data:
        #     widgets_data = request.data['widgets']
        #     for widget_data in widgets_data:
        #         widget = Widget.objects.get(id=widget_data)
        #         widget.state = instance
        #         widget.save()

        response = serializer.to_representation(instance)
        return Response(response, status=status.HTTP_200_OK)

