from django.db import transaction
from rest_framework import status

from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import mixins


from problembank.models import ProblemGroup
from problembank.serializers import ProblemGroupSerializer

from rest_framework import permissions


class ProblemGroupView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.UpdateModelMixin):
    # permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission,]

    permission_classes = [permissions.AllowAny]
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

