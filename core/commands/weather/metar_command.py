from datetime import datetime
from ..command import Command 
from .metar import Metar
from ..station import Station
from config import APIKEY
import requests
import discord


class MetarCommand(Command):

    def __init__(self):
        super().__init__(name="metar",description="Displays a METAR report for requested or nearest ICAO if the requested METAR is not found.")
        self.syntax = "$metar ICAO"

    async def execute(self, ctx, *args):
        #Initial fetch attempt
        use_nearest = False
        metar_data = self.fetch_data_from_api("metar",args[0])
            
        if not metar_data:
            #If metar_data is not found initially, set flag to try fetching nearest metar
            use_nearest = True
            metar_data = self.fetch_data_from_api("metar",args[0],use_nearest)
            
        if metar_data:
            #If metar_data is found, fetch station_data from metar report
            metar = Metar(metar_data)
            station_data = self.fetch_data_from_api("station",metar.icao) 
            station = Station(station_data)    
            await ctx.reply(embed=self.build_embed(station,metar,use_nearest))
        else:
            #if icao is invalid or API bad response code.
            await ctx.reply(f"Could not find METAR for '{args[0]}' -> METAR is unavaliable or ICAO not valid.")             

    def fetch_data_from_api(self, type, icao, nearest=False):
        #flag decides to fetch requested station or nearest station.
        if nearest:
            url = f"https://api.checkwx.com/{type}/{icao}/nearest/?x-api-key=" + APIKEY
        else:
            url = f"https://api.checkwx.com/{type}/{icao}?x-api-key=" + APIKEY
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('results') == 1:
                return data
            return None
        
    def get_country_field(self, station: Station) -> str:
        """Format the embed country field with flag emoji and name"""
        if station.country_code:
            flag_emoji = f":flag_{station.country_code.lower()}:"
            return f"{flag_emoji} {station.country_name}"
        return station.country_name or "Unknown Country"

    def build_embed(self, station: Station, metar: Metar, nearest) -> discord.Embed:
        embed = discord.Embed(
            title=f"{station.icao} METAR",
            description=f"{ "`NEAREST STATION METAR.`" if nearest else "\n" }\n\nLatest report is __{metar.age} minutes old__.\n```\n{metar.report}\n\n```",
            colour=0x00b0f4,
            timestamp=datetime.now()
        )
        embed.set_author(name="NaviBot")
        
        embed.add_field(name="Name", value=station.name or "N/A", inline=True)
        embed.add_field(name="Country", value=self.get_country_field(station), inline=True)
        embed.add_field(name="Elevation", value=f"{station.elevation_feet} ft" or "N/A", inline=True)
        
        embed.set_thumbnail(url="https://dmark.dev/public_assets/operational.jpg" if station.status == "Operational" else "https://dmark.dev/public_assets/uknown.jpg")
        embed.set_footer(text="Data provided by CheckWX", icon_url="")

        return embed
    
