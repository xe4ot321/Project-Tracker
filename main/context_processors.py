from django.conf import settings


def google_oauth_context(request):
    google_app = settings.SOCIALACCOUNT_PROVIDERS.get('google', {}).get('APP', {})
    return {
        'google_oauth_configured': bool(
            google_app.get('client_id') and google_app.get('secret')
        )
    }