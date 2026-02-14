from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from app.users.serializers import (
    RequestResetSerializer,
    VerifyCodeSerializer,
    SetNewPasswordSerializer
)


from app.users.models import User
from app.users.serializers import RegisterSerializers, UserProfileSerializers

class RegisterAPI(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers

class ProfileAPI(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [IsAuthenticated]

class RequestResetAPI(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = RequestResetSerializer



class VerifyCodeAPI(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = VerifyCodeSerializer

class SetNewPasswordAPI(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SetNewPasswordSerializer
