from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


# Custom throttle classes for auth endpoints
class LoginRateThrottle(AnonRateThrottle):
    rate = '5/minute'


class RegisterRateThrottle(AnonRateThrottle):
    rate = '3/hour'

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    AddressSerializer
)
from .models import Address

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    POST /api/auth/register/
    Rate limited to 3 registrations per hour per IP.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    throttle_classes = [RegisterRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API endpoint for user login.
    POST /api/auth/login/
    Rate limited to 5 login attempts per minute per IP.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Login successful.'
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API endpoint for user logout (blacklist refresh token).
    POST /api/auth/logout/
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'message': 'Logout successful.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve or update user profile.
    GET/PUT /api/auth/profile/
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    API endpoint to change user password.
    POST /api/auth/change-password/
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Password changed successfully.'
        }, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """
    API endpoint to request password reset.
    Sends email with reset link.
    POST /api/auth/password-reset/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        # Generate reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build reset URL (frontend URL)
        reset_url = f"{settings.CORS_ALLOWED_ORIGINS[0]}/reset-password/{uid}/{token}"

        # Send email
        subject = 'Password Reset Request - SmartSales365'
        message = render_to_string('users/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
        })

        send_mail(
            subject=subject,
            message='',
            html_message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({
            'message': 'Password reset email sent successfully.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    API endpoint to confirm password reset.
    POST /api/auth/password-reset-confirm/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {'error': 'Invalid reset link.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check token validity
        if not default_token_generator.check_token(user, serializer.validated_data['token']):
            return Response(
                {'error': 'Invalid or expired reset link.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'message': 'Password reset successful.'
        }, status=status.HTTP_200_OK)


class AddressListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list or create user addresses.
    GET/POST /api/auth/addresses/
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update or delete a specific address.
    GET/PUT/DELETE /api/auth/addresses/{id}/
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
