from argon2 import PasswordHasher

# Create a PasswordHasher instance
ph = PasswordHasher()

# Hash a password
password = "aluno"
hash = ph.hash(password)

print(hash)
# Verify the password
is_valid = ph.verify(hash, "aluno")

print(is_valid) # True if the password matches the hash