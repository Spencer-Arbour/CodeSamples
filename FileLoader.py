import json


class LoadFileContent:

    @staticmethod
    def load_json(file_name: str) -> json:
        with open(file_name, 'r') as file_to_read:
            return json.load(file_to_read)
