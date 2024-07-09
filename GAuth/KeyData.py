import base64

class KeyData:
    def __init__(self, account,secret, issuer=None, algorithm='SHA1', digits=6, interval=30):
        """
        Initialize the TOTP KeyData object.

        :param secret: The secret key for generating TOTP codes.
        :param issuer: The issuer of the TOTP (optional).
        :param account_name: The name of the account associated with the TOTP (optional).
        :param algorithm: The hash algorithm used by the TOTP. Common values are 'SHA1', 'SHA256', 'SHA512'.
        :param digits: The length of the TOTP code, typically 6 or 8 digits.
        :param interval: The time step in seconds for which each TOTP code is valid, commonly 30 seconds.
        """
        self.secret = secret
        self.issuer = issuer
        self.account = account
        self.algorithm = algorithm
        self.digits = digits
        self.interval = interval

    def __str__(self):
        """
        String representation of the KeyData object, for debugging and logging, or importing.
        """
        return f"otpauth://totp/{self.account}?secret={self.secret}&issuer={self.issuer}&algorithm={self.algorithm}&digits={self.digits}&period={self.interval}"
        
    def to_dict(self):
        """
        Serialize the KeyData object to a dictionary.
        """
        return {
            'secret': self.secret,
            'issuer': self.issuer,
            'account': self.account,
            'algorithm': self.algorithm,
            'digits': self.digits,
            'interval': self.interval,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Deserialize a dictionary into a KeyData object.
        """
        return cls(**data)