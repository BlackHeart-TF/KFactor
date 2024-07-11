import ujson as json
from ucryptolib import aes
import os

# AES requires 16-byte blocks for encryption/decryption
def pad(data):
    return data + b" " * (16 - len(data) % 16)

def encrypt_data(key, data):
    cipher = aes(key, 1)  # 1 for ECB mode
    return cipher.encrypt(pad(data))

def decrypt_data(key, data):
    cipher = aes(key, 1)  # 1 for ECB mode
    return cipher.decrypt(data).rstrip()

# Serialize and encrypt data, then write to file
def write_encrypted_file(filename, key, data):
    serialized_data = json.dumps(data).encode()
    encrypted_data = encrypt_data(key, serialized_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

# Read and decrypt data from file, then deserialize
def read_encrypted_file(filename, key):
    try:
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = decrypt_data(key, encrypted_data)
        #print(decrypted_data)
        return json.loads(decrypted_data.decode())
    except ValueError as e:  # Catch JSON errors, which may indicate key issues
        print("Failed to parse JSON. Wrong key or corrupted data?")
        return -1
    except OSError:
        # The file does not exist
        return None
    except Exception as e:  # Catch-all for other potential issues
        print(e)
        return None

if __name__ == "__main__":
    # Example usage
    key = b"yourFbytekeyhere"  # AES key must be 16, 24, or 32 bytes
    data = [("example_list", "asdasd"), ("example_string", "Hello, world!")]

    # Write encrypted data to file
    write_encrypted_file("encrypted_data.json", key, data)

    # Read encrypted data from file
    retrieved_data = read_encrypted_file("encrypted_data.json", key)
    print(retrieved_data)

