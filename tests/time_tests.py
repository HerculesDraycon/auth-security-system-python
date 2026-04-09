import time
import hashlib
import bcrypt
import os

senha = "123456"

# ---------------- MD5 ----------------
start = time.time()
for _ in range(100000):
    hashlib.md5(senha.encode()).hexdigest()
end = time.time()

print("MD5 tempo:", end - start)


# ---------------- SHA256 + SALT ----------------
start = time.time()
for _ in range(100000):
    salt = os.urandom(16).hex()
    hashlib.sha256((senha + salt).encode()).hexdigest()
end = time.time()

print("SHA256 + Salt tempo:", end - start)


# ---------------- BCRYPT ----------------
start = time.time()
for _ in range(100):
    bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
end = time.time()

print("Bcrypt tempo:", end - start)