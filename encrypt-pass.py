import bcrypt

password = "doeuspjlzhavelwe"

# Encode password into a readable utf-8 byte code:
password = password.encode('utf-8')

# Hash the ecoded password and generate a salt:
hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashedPassword)