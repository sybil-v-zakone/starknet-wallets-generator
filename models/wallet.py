import json
from dataclasses import dataclass


@dataclass
class Wallet:
    def __init__(
            self,
            address: str,
            private_key: str,
            seed: str
    ):
        self.address = address
        self.private_key = private_key
        self.seed = seed

    def to_json(self):
        try:
            return json.dumps(self, default=lambda o: o.__dict__)
        except Exception as e:
            print(f"Model to json object error: {str(e)}")
