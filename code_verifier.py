import hashlib
import os
import base64

# Generate code verifier
def generate_code_verifier():
    # Generate a secure random string
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8').rstrip('=')
    return code_verifier

# Generate code challenge from code verifier
def generate_code_challenge(code_verifier):
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')
    return code_challenge

# Generate and print code_verifier and code_challenge
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

print("Code Verifier:", code_verifier)
print("Code Challenge:", code_challenge)
