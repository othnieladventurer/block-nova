from coinbase.rest import RESTClient
from django.conf import settings

def get_coinbase_client():
    return RESTClient(
        api_key=settings.COINBASE_CDP_API_KEY_ID,
        api_secret=settings.COINBASE_CDP_API_SECRET_KEY,
        environment=settings.COINBASE_CDP_ENVIRONMENT
    )
