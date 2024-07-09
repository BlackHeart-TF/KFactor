import hmac
import hashlib, binascii, time

from encryptfile import read_encrypted_file
from GAuth.KeyData import KeyData

currentcode = 0
currentkey = None
totalkeys = 1

last_key = 0

user_key = None

def base32_decode(encoded):
    base32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    
    # Convert the Base32 encoded string to a string of bits
    bits = ""
    for char in encoded:
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

def read_file(user_key):
    with open("/flash/certificate/key.totp", 'r') as file:
        basekey = file.read().strip()
    salted = bytes(user_key)+basekey.encode()
    hash_obj = uhashlib.sha256(salted)
    hash_bytes = hash_obj.digest()[:32]  # Get the binary hash value
    keyfile = read_encrypted_file("/flash/totpdata",hash_bytes)
    return keyfile if keyfile is not None and keyfile != -1 else None
    
def get_key(index):
    global totalkeys,user_key
    keyfile = read_file(user_key)
    if not keyfile:
        return None
    keys = [KeyData.from_dict(key) for key in keyfile]
    print(keys[index])
    totalkeys = len(keys)
    print("totalkeys: "+str(totalkeys))
    print("index"+str(index))
    return keys[index] if index < len(keys) else None

def generate_totp(secret, time_step=30, digits=6):
    # Ensure 'secret' is a bytearray (decoded from Base32)
    # Calculate the TOTP counter
    counter = int(time.time() // time_step)
    # Convert counter to byte array in big-endian order
    counter_bytes = counter.to_bytes(8, 'big')
    # Create HMAC object with SHA-1
    hmacc = libs.hmac.new(secret, counter_bytes, 'sha1')
    hmac_digest = hmacc.digest()
    # Dynamic truncation
    offset = hmac_digest[-1] & 0x0F
    code = hmac_digest[offset:offset+4]
    code = ((code[0] & 0x7f) << 24) | (code[1] << 16) | (code[2] << 8) | code[3]
    # Generate the OTP
    otp = code % (10 ** digits)
    padded = f"{code % (10 ** digits):0{digits}d}"
    return padded

def setup():
    global currentkey,last_key
    last_key = time.time()
    currentkey = get_key(0)

def display_totp(secret):
    print(secret.account)
    decoded = base32_decode(secret.secret)
    bytestr = binascii.hexlify(decoded)
    #print("decoded: "+str(bytestr))
    code = generate_totp(decoded)
    print(str(code))

def update_display():
    if currentkey:
        display_totp(currentkey)

def btnA_wasClicked_event(state):
    global currentcode,currentkey,totalkeys,last_key
    print("A Button!!")
    currentcode -= 1
    if currentcode < 0:
        currentcode = totalkeys-1
    currentkey = get_key(currentcode)
    last_key = time.time()

def btnC_wasClicked_event(state):
    global currentcode, currentkey,totalkeys,last_key
    print("C Button!!")
    currentcode += 1
    if currentcode >= totalkeys:
        currentcode = 0
    currentkey = get_key(currentcode)
    last_key = time.time()

def check_touch():
    global last_key
    points = M5.Touch.getCount()
    print(f"points: {points}")
    if points:  # If there's a touch
        t = M5.Touch.getTouchPointRaw()
        print(t)
        x, y = t[0], t[1]
        if x < 100:  # Check if touch is within button region
            btnA_wasClicked_event(None)
            time.sleep_ms(500)
        elif x > 220:
            btnC_wasClicked_event(None)
            time.sleep_ms(500)
        else:
            last_key = time.time()  # Reset the timer on touch



def loop():
    global last_key
    update_display()
    check_touch()

def TryDecryptKeys(pin): #the password acceptance function
    global user_key
    keyfile = read_file(pin)
    success = keyfile != None #pin == [0,1,2,3]
    print(f"returned: {success}")
    if success:
        user_key = pin
    return success;

def Run():
    try:
        setup()
        while True:
            loop()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    Run()
