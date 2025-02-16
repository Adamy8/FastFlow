import secrets

# Generate a random 256-bit key (32 bytes)
random_secret_key = secrets.token_hex(32)
print(random_secret_key)
