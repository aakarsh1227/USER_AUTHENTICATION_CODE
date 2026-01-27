from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    Utility Wrapper: Handles the generation of JWT tokens.
    This is used during Registration and Login to provide the user their 'Passport'.
    """
    
    # 1. Generate a Refresh Token for the specific user instance
    refresh = RefreshToken.for_user(user)
    
    # 2. Add Custom Claims (Security Integrity)
    # We 'wrap' extra data inside the token so the frontend doesn't 
    # need to call the database to check status.
    refresh['username'] = user.username
    refresh['is_verified'] = user.is_active 
    
    # 3. Return the pair as strings
    # 'access' is for the Authorization header (15 mins)
    # 'refresh' is for getting a new access token (24 hours)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }