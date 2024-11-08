import json
class JSONReader:
    def __init__(self, json_data):
        if isinstance(json_data, str):
            self.data = json.loads(json_data)
        else:
            self.data = json_data

    def get_all_values(self, data=None, skip_levels=0):
        if data is None:
            data = self.data

        result = {}

        def flatten(d, parent_key='', level=0):
            if level < skip_levels:
                next_key = ''
            else:
                next_key = parent_key

            if isinstance(d, dict):
                for k, v in d.items():
                    new_key = f"{next_key}_{k}" if next_key else k
                    flatten(v, new_key, level + 1)
            elif isinstance(d, list):
                for i, item in enumerate(d):
                    new_key = f"{next_key}_{i}" if next_key else str(i)
                    flatten(item, new_key, level + 1)
            else:
                result[next_key] = d

        flatten(data)
        return result
