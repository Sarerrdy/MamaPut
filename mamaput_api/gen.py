# import secrets

# Generate a strong secret key
# secret_key = secrets.token_urlsafe(32)
# print(secret_key)

from werkzeug.security import generate_password_hash

key = generate_password_hash('hjndh87364485')
print(key)
