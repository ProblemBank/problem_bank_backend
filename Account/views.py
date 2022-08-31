from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import User


# todo:
# GenericAPIView

class CreateUserAPI(generics.ListCreateAPIView):
    def get_queryset(self):
        return User.objects.all()

    serializer_class = CreateUserSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({"user": serializer.data})


class ChangePasswordAPI(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.users

    def put(self, request, *args, **kwargs):
        self.object = self.request.users
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"msg": 1}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        alldatas = {}
        if serializer.is_valid(raise_exception=True):
            mname = serializer.save()
            alldatas['message'] = 'رمز با موفقیت تغییر پیدا کرد'
            print(alldatas)
            return Response(alldatas)

        return Response('خطا، لطفا دوباره تلاش کنید')
