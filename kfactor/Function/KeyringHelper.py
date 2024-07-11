import json
import keyring

class KeyringHelper:
    def __init__(self, service_name):
        self.service_name = service_name

    def store_totp_entry(self, sub_key, totp_data):
        entries = self.retrieve_entries()
        if not entries:
            entries = {}
        
        entries[sub_key] = totp_data
        self.store_entries(entries)

    def retrieve_totp_entry(self, sub_key):
        entries = self.retrieve_entries()
        if entries and sub_key in entries:
            return entries[sub_key]
        return None

    def retrieve_entries(self):
        entries_json = keyring.get_password(self.service_name, self.service_name)
        if entries_json:
            return json.loads(entries_json)
        return {}

    def store_entries(self, entries):
        entries_json = json.dumps(entries)
        keyring.set_password(self.service_name, self.service_name, entries_json)

# Example usage:
if __name__ == "__main__":
    helper = TOTPKeyringHelper("MyApp")

    # Store TOTP entries for index "users"
    index_key = "users"
    sub_key1 = "user1"
    sub_key2 = "user2"

    totp_data1 = {
        "issuer": "Example1",
        "label": "user1@example.com",
        "secret": "12345678901234567890",
        "digits": 6,
        "algorithm": "SHA1",
        "period": 30
    }

    totp_data2 = {
        "issuer": "Example2",
        "label": "user2@example.com",
        "secret": "09876543210987654321",
        "digits": 6,
        "algorithm": "SHA256",
        "period": 30
    }

    helper.store_totp_entry(index_key, sub_key1, totp_data1)
    helper.store_totp_entry(index_key, sub_key2, totp_data2)

    # Retrieve TOTP entry for user1
    retrieved_data1 = helper.retrieve_totp_entry(index_key, sub_key1)
    if retrieved_data1:
        print("Retrieved TOTP Data for user1:")
        print(json.dumps(retrieved_data1, indent=4))

    # Retrieve TOTP entry for user2
    retrieved_data2 = helper.retrieve_totp_entry(index_key, sub_key2)
    if retrieved_data2:
        print("Retrieved TOTP Data for user2:")
        print(json.dumps(retrieved_data2, indent=4))
