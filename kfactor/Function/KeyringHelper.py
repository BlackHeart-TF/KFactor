import json
import keyring

class KeyringHelper:
    def __init__(self, service_name):
        self.service_name = service_name

    def store_totp_entry(self, totp_data):
        entries = self.retrieve_entries()
        if not entries:
            entries = {}
        sub_key:str = totp_data.account
        entries[sub_key] = totp_data.to_dict()
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

