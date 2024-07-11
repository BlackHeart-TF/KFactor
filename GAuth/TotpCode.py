class TotpCode:
    import time,hmac
    def __init__(self, account,secret, issuer=None, algorithm='SHA1', digits=6, period=30):
        """
        Initialize the TOTP KeyData object.

        :param secret: The secret key for generating TOTP codes.
        :param issuer: The issuer of the TOTP (optional).
        :param account_name: The name of the account associated with the TOTP (optional).
        :param algorithm: The hash algorithm used by the TOTP. Common values are 'SHA1', 'SHA256', 'SHA512'.
        :param digits: The length of the TOTP code, typically 6 or 8 digits.
        :param interval: The time step in seconds for which each TOTP code is valid, commonly 30 seconds.
        """
        self.secret = TotpCode.base32_decode(secret)
        self.issuer = issuer
        self.account = account
        self.algorithm = algorithm
        self.digits = int(digits)
        self.period = int(period)

    def base32_decode(encoded:str):
        base32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
        
        # Convert the Base32 encoded string to a string of bits
        bits = ""
        for char in encoded.upper().rstrip('=\x00'):
            if char in base32_alphabet:
                # Find the index of the char in the alphabet
                index = base32_alphabet.index(char)
                # Convert that index to a binary string, manually ensuring it's 5 bits
                binary_str = bin(index)[2:]
                while len(binary_str) < 5:  # Manually pad with leading zeros
                    binary_str = '0' + binary_str
                bits += binary_str
            else:
                raise ValueError("Invalid character found: " + char)
             # Convert the bit string to bytes
        decoded_bytes = bytearray()
        for i in range(0, len(bits), 8):  # Process 8 bits at a time
            byte_segment = bits[i:i+8]
            if len(byte_segment) < 8:
                # If we have fewer than 8 bits left, pad with zeros to the right
                byte_segment = byte_segment + '0' * (8 - len(byte_segment))
            decoded_bytes.append(int(byte_segment, 2))

        return bytes(decoded_bytes)

    def GetCode(self):
        # Calculate the TOTP counter
        counter = int(TotpCode.time.time() // self.period)
        # Convert counter to byte array in big-endian order
        counter_bytes = counter.to_bytes(8, 'big')
        # Create HMAC object with SHA-1
        hmacc = TotpCode.hmac.new(self.secret, counter_bytes, 'sha1')
        hmac_digest = hmacc.digest()
        # Dynamic truncation
        offset = hmac_digest[-1] & 0x0F
        code = hmac_digest[offset:offset+4]
        code = ((code[0] & 0x7f) << 24) | (code[1] << 16) | (code[2] << 8) | code[3]
        # Generate the OTP
        otp = code % (10 ** self.digits)
        padded = f"{code % (10 ** self.digits):0{self.digits}d}"
        return padded
    
    def GetInterval(self):
        # Calculate the percentage within the current interval
        percentage = (TotpCode.time.time() % self.period) / self.period
        
        # Convert percentage to a range of 1-100
        interval_percentage = 100-int(percentage * 100) 
        return interval_percentage

    def __str__(self):
        """
        String representation of the KeyData object, for debugging and logging, or importing.
        """
        from GAuth.GAuth import encode_base32
        return f"otpauth://totp/{self.account}?account={self.account}&secret={encode_base32(self.secret)}&issuer={self.issuer}&algorithm={self.algorithm}&digits={self.digits}&period={self.period}"
        
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
            'period': self.period,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Deserialize a dictionary into a KeyData object.
        """
        return cls(**data)
    
    @classmethod
    def from_otpauth(cls, uri:str):
        """
        Deserialize a Uri into a KeyData object.
        """
        from GAuth.GAuth import parse_url_query
        codes = parse_url_query(uri)
        return cls(**codes['query'])