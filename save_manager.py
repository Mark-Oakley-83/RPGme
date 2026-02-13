import json
from datetime import datetime
import os
#AI generated code (unconfirmed)
class SaveManager:
    def __init__(self, character_name):
        self.char_name = character_name.replace(" ", "_") # Ensure no spaces in filenames
        self.date_str = datetime.now().strftime("%Y-%m-%d")
        # Inside SaveManager __init__
        self.folder = f"character_saves/{self.char_name}"
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def save_master(self, data):
        """Saves the definitive character state."""
        filename = f"{self.char_name}_master_{self.date_str}.json"
        self._write_file(filename, data)

    def save_snapshot(self, data, session_note=""):
        """Saves a campaign-specific snapshot."""
        # Optional: include a session note or increment for multiple snapshots per day
        filename = f"{self.char_name}_campaign_snapshot_{self.date_str}.json"
        self._write_file(filename, data)

    def _write_file(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"File saved: {filename}")

if __name__ == "__main__":
    save_manager()