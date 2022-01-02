import os
def generate_password(size):
    password = ""
    chars = [(48, 57), (65, 90), (97, 122)]
    for i in range(size):
        j = ord(os.urandom(1)) % 3
        password += chr(ord(os.urandom(1)) % (chars[j][1] - chars[j][0]) + chars[j][0])
    return password
