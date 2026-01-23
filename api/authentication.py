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


def generate_tokens_for_user(user):
    """
    Generate JWT access and refresh tokens for CustomUser.
    """
    # Access Token (6 hours)
    access_payload = {
        'user_id': user.id,
        'email': user.email,
        'role': user.role,
        'token_type': 'access',
        'exp': datetime.utcnow() + timedelta(hours=6),
        'iat': datetime.utcnow(),
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    
    # Refresh Token (7 days)
    refresh_payload = {
        'user_id': user.id,
        'token_type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
    
    return {
        'access': access_token,
        'refresh': refresh_token,
    }


def refresh_access_token(refresh_token):
    """
    Generate new access token using refresh token.
    """
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        
        if payload.get('token_type') != 'refresh':
            raise exceptions.AuthenticationFailed('Invalid token type')
        
        user = CustomUser.objects.get(id=payload['user_id'], is_active=True)
        
        # Generate new access token
        access_payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'token_type': 'access',
            'exp': datetime.utcnow() + timedelta(hours=6),
            'iat': datetime.utcnow(),
        }
        new_access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
        
        return {'access': new_access_token}
        
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Refresh token has expired')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid refresh token')
    except CustomUser.DoesNotExist:
        raise exceptions.AuthenticationFailed('User not found')
