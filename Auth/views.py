from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password

from .models import Auth
from .serializer import SignupSerializer, LoginSerializer
from .utils import generate_jwt_token


class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request, *args, **kwargs):

        serializer = SignupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if Auth.objects.filter(email=email).exists():
            return Response(
                {"details": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Auth.objects.filter(username=username).exists():
            return Response(
                {"details": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        hashed_password = make_password(password)
        user = Auth.objects.create(
            username=username,
            email=email,
            password=hashed_password
        )

        return Response(
            {"details": "User created successfully", "username": user.username},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = Auth.objects.filter(email=email).first()

        if user:
            if check_password(password, user.password):
                token = generate_jwt_token(useremail=user.email)
                return Response(
                    {"details": {"AccessToken": token, "UserID": user.id}},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"details": "Incorrect password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {"details": "No user found for provided email"},
                status=status.HTTP_404_NOT_FOUND
            )
        