import bcrypt

class Hash:
    @staticmethod
    def bcrypt(password: str):
        # bcrypt requires bytes, so encode the password
        # gensalt() generates a salt
        # hashpw returns bytes, so decode to string for storage
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify(plain_password, hashed_password):
        # bcrypt.checkpw requires bytes
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
