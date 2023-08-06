import json
import requests

class Amplitude:

    def __init__(self, api_key):
        self.url = "https://api.amplitude.com/identify"
        self.api_key = api_key
    
    @staticmethod
    def _parse(key):
        return key.split(":")

    def post(self, key, value):

        _, ab_test_id, user_id = self._parse(key)

        user_properties = {
            f"abTest.{ab_test_id}": value.get("ab_test_group")
        }

        data = {
            "api_key": self.api_key,
            "identification": json.dumps(
                [
                    {
                        "user_id": user_id,
                        "user_properties": user_properties
                    }
                ]
            )
        }

        response = requests.post(self.url, data=data)