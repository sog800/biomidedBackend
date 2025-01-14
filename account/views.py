from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated



class RegisterView(APIView):
    permission_classes = []  # No permissions required

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        # Collect error messages
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")

        # Send detailed error messages to the frontend
        return Response(
            {"message": "Registration failed", "errors": error_messages},
            status=status.HTTP_400_BAD_REQUEST,
        )



# Login View
class LoginView(APIView):
    permission_classes = []  # No permissions required
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)




class LogoutView(APIView):
    

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Log headers for debugging
        print("Authorization Header:", request.headers.get("Authorization"))

        try:
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
                return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No active session found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Failed to log out"}, status=status.HTTP_400_BAD_REQUEST)
        



from .models import UserInfo
from .serializers import UserInfoSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = UserInfo.objects.get_or_create(user=request.user)
        serializer = UserInfoSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile, _ = UserInfo.objects.get_or_create(user=request.user)
        serializer = UserInfoSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
