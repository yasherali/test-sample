import hmac, hashlib, base64
from django.conf import settings

def is_valid_shopify_hmac(data, hmac_header):
    secret = settings.SHOPIFY_SHARED_SECRET.encode('utf-8')
    digest = hmac.new(secret, data.encode('utf-8'), hashlib.sha256).digest()
    calculated_hmac = base64.b64encode(digest).decode()
    return hmac.compare_digest(calculated_hmac, hmac_header)