from django.core.management.utils import get_random_secret_key
import secrets

# You can run this script to generate a Django SECRET_KEY and a JWT signing key.

print("Django SECRET_KEY:")
print(get_random_secret_key())

print("\nJWT_SIGNING_KEY:")
print(secrets.token_urlsafe(64))