import secrets
import string


def generate_api_key(length=64):
    alphabet = string.ascii_letters + string.digits
    key = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"sk_{key}"


api_key = generate_api_key()
print(api_key)
