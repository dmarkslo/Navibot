from ...jsonreader import JSONReader
from ...entity import Entity
from datetime import datetime, timezone
from math import floor

class Metar(Entity):
    items = [
        'report'
    ]

    def __init__(self, data):
        """Flatten data before we initialize Entity 
        and change API return data key '0' to 'value' for clarity."""
        jsonReader = JSONReader(data)
        flat_data = jsonReader.get_all_values(None,2)
        flat_data["report"] = flat_data.pop("0")
        super().__init__(flat_data)
        self.datetime = self.decodeDateTime()
        self.age = self.calculateReportAge()
        self.icao = self.decodeICAO()

    def decodeICAO(self):
        return self.report.split()[0]

    def decodeDateTime(self):
        value = self.report.split()[1]
        day = int(value[:2]) 
        hour = int(value[2:4])  
        minute = int(value[4:6])  

        today_date = datetime.now(timezone.utc).date()

        # Combine day, hour, minute to a datetime object
        report_utc_datetime = datetime(today_date.year, today_date.month, day, hour, minute, tzinfo=timezone.utc)
        return report_utc_datetime

    def calculateReportAge(self):
       curr_utc_datetime = datetime.now(timezone.utc)  
       return floor((curr_utc_datetime - self.datetime).total_seconds() / 60)


        
        