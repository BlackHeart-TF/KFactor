import json
import keyring

class KeyringHelper:
    def __init__(self, service_name):
        self.service_name = service_name

    def add_entry(self, totp_data):
        entries = self.retrieve_entries()
        if not entries:
            entries = {}
        sub_key = max([int(entry) for entry in entries.keys()]+[0]) +1
        entries[sub_key] = totp_data.to_dict()
        self.store_entries(entries)
        return sub_key

    def update_entry(self,id, totp_data):
        entries = self.retrieve_entries()
        if not entries:
            return
        entries[id] = totp_data.to_dict()
        self.store_entries(entries)

    def remove_entry(self,id):
        entries = self.retrieve_entries()
        if not entries or id not in entries:
            return
        del entries[id]
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

