import bcrypt

class Encryption:
    KEY=b'$2b$12$rhqAk4.BjC.3MK2Xe6epH.'
    
    @classmethod
    def encrypt(self,password: str)->bytes:
        """
        Encrypts a given text using a certain KEY/salt.
        uses bcrypt.
        """

        password=password.encode('UTF-8')
        return bcrypt.hashpw(password,self.KEY)

    @classmethod
    def decrypt(self,real_password: bytes, password_attempt: str)->bool:
        """
        Decrypts hashed_text and compares with a given text.
        Returns True if matched, False if not
        """
        password_attempt: bytes =password_attempt.encode('UTF-8')
        return bcrypt.checkpw(password_attempt, real_password)
