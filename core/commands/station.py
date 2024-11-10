from ..jsonreader import JSONReader
from ..entity import Entity

class Station(Entity):
    items = [
        'icao',
        'city',
        'country_code',
        'country_name',
        'elevation_feet',
        'elevation_meters',
        'geometry_coordinates_0',
        'geometry_coordinates_1',
        'geometry_type',
        'iata',
        'latitude_decimal',
        'latitude_degrees',
        'longtitude_decimal',
        'longtitude_degrees',
        'location',
        'name',
        'region_code',
        'region_name',
        'state_code',
        'state_name',
        'status',
        'type',
    ]

    def __init__(self, data):
        """Flatten data before we initialize Entity"""
        jsonReader = JSONReader(data)
        flat_data = jsonReader.get_all_values(None,3)
        super().__init__(flat_data)
