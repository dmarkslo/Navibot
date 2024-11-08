from .entity import Entity
from .jsonreader import JSONReader

class Metar(Entity):
    items = [
        'value'
    ]

    def __init__(self, data):
        """Flatten data before we initialize Entity 
        and change API return data key '0' to 'value' for clarity."""
        jsonReader = JSONReader(data)
        flat_data = jsonReader.get_all_values(None,2)
        flat_data["value"] = flat_data.pop("0")
        super().__init__(flat_data)

   