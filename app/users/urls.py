from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenBlacklistView
)
from app.users.views import RegisterAPI, ProfileAPI, RequestResetAPI, VerifyCodeAPI, SetNewPasswordAPI

router = DefaultRouter()
router.register(r"register", RegisterAPI, basename='register')
router.register(r"profile", ProfileAPI, basename='profile')

urlpatterns = [
    path("password-reset/", RequestResetAPI.as_view({"post": "create"})),
    path("password-verify/", VerifyCodeAPI.as_view({"post": "create"})),
    path("password-set/", SetNewPasswordAPI.as_view({"post": "create"})),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", TokenBlacklistView.as_view()),
]

urlpatterns += router.urls
