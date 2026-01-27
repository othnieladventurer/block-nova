from cdp import CdpClient
from django.conf import settings

def get_coinbase_client():
    # Initialize the CDP client with your API keys and environment
    return CdpClient(
        api_key=settings.COINBASE_CDP_API_KEY_ID,
        api_secret=settings.COINBASE_CDP_API_SECRET_KEY,
        environment=settings.COINBASE_CDP_ENVIRONMENT  # "sandbox" or "production"
    )
