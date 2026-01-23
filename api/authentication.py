"""
Custom JWT Authentication for CustomUser model.
This allows API to use CustomUser while Django Admin uses default auth.User.
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import authentication, exceptions
from ecommerce.models import CustomUser


class CustomUserJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication that works with CustomUser model (ecommerce.models)
    instead of Django's default auth.User.
    """
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        try:
            # Extract token from "Bearer <token>"
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None
        
        try:
            # Decode the JWT token
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            
            # Get user from CustomUser model
            user_id = payload.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed('Invalid token payload')
            
            user = CustomUser.objects.get(id=user_id, is_active=True)
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
    
    def authenticate_header(self, request):
        return 'Bearer'


from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# ... (CustomUserJWTAuthentication remains mostly same but we can rely on verifying signature using simplejwt if needed, 
#      but for now let's stick to fixing GENERATION first as requested. 
#      Actually, we should update decoding too if the key/algo changes, but simplejwt uses settings.SECRET_KEY too.)

def generate_tokens_for_user(user):
    """
    Generate JWT access and refresh tokens for CustomUser using simplejwt.
    This ensures all standard claims (jti, exp, iat) are present.
    """
    refresh = RefreshToken.for_user(user)
    
    # Add custom claims
    refresh['email'] = user.email
    refresh['role'] = getattr(user, 'role', 'customer')
    
    # Access token is automatically created from refresh token with same claims
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def refresh_access_token(refresh_token_str):
    """
    Generate new access token using refresh token via simplejwt.
    """
    try:
        # Verify and create RefreshToken object
        refresh = RefreshToken(refresh_token_str)
        
        # simplejwt handles expiration and validity check internally
        
        new_access_token = refresh.access_token
        
        return {'access': str(new_access_token)}
        
    except TokenError as e:
        raise exceptions.AuthenticationFailed(f'Invalid or expired refresh token: {e}')
