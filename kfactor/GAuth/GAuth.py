import base64
from .TotpCode import TotpCode,Algorithm,DigitCount
    
def parse_url_query(url):
    result = {
        'proto': '',
        'url': '',
        'query': {}
    }
    
    # Split protocol
    if '://' in url:
        parts = url.split('://', 1)
        result['proto'] = parts[0]
        url = parts[1]
    else:
        result['proto'] = "otpauth"
    
    # Split URL and query string
    parts = url.split('?', 1)
    result['url'] = parts[0]
    
    # Parse query string
    if len(parts) > 1:
        query_str = parts[1]
        pairs = query_str.split('&')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                result['query'][key] = value.strip("\"")                
    return result

def simple_url_decode(s):
    replacements = {
        '%20': ' ',   # Space
        '%3D': '=',   # Equals sign
        '%26': '&',   # Ampersand
        '%3F': '?',   # Question mark
        '%2B': '+',   # Plus sign
        '%2F': '/'    # Forward slash
    }
    for src, dest in replacements.items():
        s = s.replace(src, dest)
    return s

def parse_url_query_with_decoding(url):
    url = simple_url_decode(url)
    return parse_url_query(url)

def decode_base64(encoded_str):
    # If the string is URL-safe base64 encoded, decode
    # and add necessary padding
    adjusted_str = simple_url_decode(encoded_str) 
    #print(adjusted_str)
    padding_needed = len(adjusted_str) % 4
    if padding_needed:  # Add padding if necessary
        adjusted_str += '=' * (4 - padding_needed)
    
    try:
        decoded_bytes = base64.b64decode(adjusted_str)
        try:
            # Attempt to decode as UTF-8 text if possible
            return decoded_bytes.decode('utf-8')
        except Exception:
            # Return as bytes if it cannot be decoded to text
            return decoded_bytes
    except Exception as e: 
        print(f"Error decoding Base64: {e}")
        return None

def encode_base32(input_bytes):
    
    # Encode these bytes in base32
    encoded_bytes = base64.b32encode(input_bytes)
    
    # Convert the base32 encoded bytes back to a string
    encoded_string = encoded_bytes.decode('utf-8')
    
    return encoded_string

def parseExportData(data):
    if data[0] != 10:
        print(f"Invalid data. First char expected '10' (newline) got {data[0]}")
        return
    entry_len = 0
    index = 0
    more = True
    list = []
    while more:
        entry_len =  data[index+1] #seems to be length starting after key
        val = hex(data[entry_len]),hex(data[entry_len+1]),hex(data[entry_len+2]),hex(data[entry_len+3])
        iindex = index +1
        secret,account,issuer,algorithm,digits,period = None,None,None,"SHA1",6,30
        hex_string = ''.join([f'{byte:02x} ' for byte in data])
        print(hex_string)
        hex_string = ''.join([f'{byte} ' for byte in data])
        for b in data:
            try:
                # Decode the byte to a character if possible
                char = chr(b) if 0x20 <= b < 0x7F else '.'
                print(f"{b:02x} {b} {char}")
            except UnicodeDecodeError:
                # Use '.' for bytes that can't be decoded
                print(f"{b:02x} {b} .")

        #print(hex_string)
        while iindex < len(data):
        #for i in range(3):
            
            fieldid = data[iindex+1]
            data_len = data[iindex+2]
            debugdata = data[iindex:iindex+3 + data_len]
            if fieldid == 10: #secret
                secret = encode_base32(data[iindex+3:iindex+3 + data_len])
            elif fieldid == 0x12: #account
                account = str(data[iindex+3:iindex+3 + data_len].decode('utf-8'))
            elif fieldid == 0x1a: #issuer
                issuer = str(data[iindex+3:iindex+3 + data_len].decode('utf-8'))
            elif fieldid == 0x20: #unknown
                algorithm = Algorithm.toAlgoString(data_len)
            elif fieldid == 0x28: #unknown
                digits = DigitCount.toCount(data_len)
            elif fieldid == 0x30: #OTPtype
                pass
            else:
                print(f"Unknown field: 0x{fieldid:X}")
            
            iindex += data_len+2
        index += entry_len+2
        val = hex(data[index-1]),hex(data[index]),hex(data[index+1]),hex(data[index+2]),hex(data[index+3])
        if data[index] == 0x10:
            more = False
        key_data = TotpCode(account,secret,issuer,algorithm,digits,period)
        list.append(key_data)
    return list

def decode_migration_urldata(url_data):
    if 'data' not in url_data['query']:
        print("Error: no data")
        return None
    key = url_data['query']['data'].rstrip('\n')
    print(key)
    return parseExportData(decode_base64(key))

def decode_import_urldata(url_data):
    if 'secret' not in url_data['query']:
        print("Error: no secret")
        return None
    
    account = url_data['url'].split('/')[-1]
    secret = url_data['query']['secret']
    issuer = url_data['query']['issuer']
    algorithm = url_data['query'].get('algorithm',"SHA1")
    digits = url_data['query'].get('digits',6)
    interval = url_data['query'].get('period',30)
    
    if algorithm.upper() != "SHA1":
        print(f"Error: only SHA1 supported, got \'{algorithm}\'")
    key = TotpCode(account,secret,issuer,algorithm,digits,interval)
    return [key]

def decode_url(url):
    url_data = parse_url_query_with_decoding(url)
    print(url)
    print(url_data)
    if url_data['proto'] == "otpauth-migration":
        return decode_migration_urldata(url_data)
    elif url_data['proto'] == "otpauth":
        return decode_import_urldata(url_data)
    else:
        return None
    





