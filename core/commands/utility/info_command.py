from datetime import datetime
from ..command import Command
from ...entity import Entity 
from ...jsonreader import JSONReader
from ..station import Station
from config import APIKEY
import requests
import discord


class InfoCommand(Command):
    #TODO: improve this, many shared methods with metar_command rn.
     
    def __init__(self):
        super().__init__(name="info", description="Displays basic airfield data.")
        self.syntax = f"${self.name} ICAO"

    async def execute(self,ctx,*args):
        station_data = self.fetch_data_from_api("station",args[0]) 
        if station_data:
            station_object = Station(station_data)    
            await ctx.reply(embed=self.build_embed(station_object))
        else:
            await ctx.reply("Requested airport not found. Make sure the ICAO is valid.")

    def fetch_data_from_api(self, type, icao):
        URL = f"https://api.checkwx.com/{type}/{icao}?x-api-key=" + APIKEY
        
        response = requests.get(URL)
        if response.status_code == 200: #200 = OK
            data = response.json()
            if data.get('results') == 1:
                return data
            return None
        
    def get_country_field(self, station: Station) -> str:
        """Format the country field with flag emoji and name"""
        if station.country_code:
            flag_emoji = f":flag_{station.country_code.lower()}:"
            return f"{flag_emoji} {station.country_name}"
        return station.country_name or "Unknown Country"

    def build_embed(self, station: Station) -> discord.Embed:
        embed = discord.Embed(
            title=f"{station.icao} AIRPORT INFORMATION",
            description=f"\nRelevant airfield data:\n\n",
            colour=0x00b0f4,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="ICAO", value=station.icao or "N/A", inline=True)
        embed.add_field(name="IATA", value=station.iata or "N/A", inline=True)
        embed.add_field(name="Type", value=station.type or "N/A", inline=True)
        embed.add_field(name="Name", value=station.name or "N/A", inline=True)
        embed.add_field(name="Location", value=station.location or "N/A", inline=True)
        embed.add_field(name="Country", value=self.get_country_field(station), inline=True)
        embed.add_field(name="Elevation (ft)", value=f"{station.elevation_feet} ft" or "N/A", inline=True)
        embed.add_field(name="Elevation (m)", value=f"{station.elevation_meters} m" or "N/A", inline=True)
        embed.add_field(name="Status", value=f"{station.status}" or "N/A", inline=True)

        embed.set_thumbnail(url="https://dmark.dev/public_assets/operational.jpg" if station.status == "Operational" else "https://dmark.dev/public_assets/uknown.jpg")
        embed.set_footer(text="Data provided by CheckWX", icon_url="")

        return embed