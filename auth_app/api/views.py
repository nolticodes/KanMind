from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import RegistrationSerializer, LoginSerializer


"""Views for user registration and token-based login."""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(APIView):
    """Create a new user account and return an authentication token."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Validate registration data, create the account, and return its token."""
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)

            data = {
                "token": token.key,
                "fullname": saved_account.fullname,
                "email": saved_account.email,
                "user_id": saved_account.id,
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
)


class LoginView(APIView):
    """Authenticate a user and return an existing or newly created token."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """Validate login credentials and return the user's authentication token."""
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "fullname": user.fullname,
                    "email": user.email,
                    "user_id": user.id,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )