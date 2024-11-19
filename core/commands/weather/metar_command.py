from datetime import datetime
from ..command import Command 
from ..metar import Metar
from ..station import Station
from config import APIKEY
import requests
import discord

#WIP:
#   - Send an embed of current METAR data to user
#      (Add Playwright functionality to screenshot webpage and send as jpg)
#       SOLVE: MAKE OWN WEBPAGE FROM EMBED WITH BUILT IN SCRIPT TO IMPORT STYLING ETC,
#       or screenshot an area from the main webpage
class MetarCommand(Command):

    def __init__(self):
        super().__init__(name="metar",description="Displays a METAR report for requested or nearest ICAO if the requested METAR is not found.")
        self.syntax = f"${self.name} ICAO"

    async def execute(self, ctx, *args):
        icao = args[0]
        #Initial fetch attempt
        use_nearest = False
        metar_data = self.fetch_data_from_api("metar",icao)
            
        if not metar_data:
            #set flag to fetch nearest metar
            use_nearest = True
            metar_data = self.fetch_data_from_api("metar",icao,use_nearest)
            
        if metar_data:
            #fetch station_data from found metar report
            metar_object = Metar(metar_data)
            station_data = self.fetch_data_from_api("station",metar_object.icao) 
            station_object = Station(station_data)    
            await ctx.reply(embed=self.build_embed(station_object,metar_object,use_nearest))
        else:
            #if icao is invalid or API bad response code.
            await ctx.reply(f"Could not find METAR for '{args[0]}' -> METAR is unavaliable or ICAO not valid.")             

    def fetch_data_from_api(self, type, icao, nearest=False):
        #flag decides to fetch requested station or nearest station.
        if nearest:
            URL = f"https://api.checkwx.com/{type}/{icao}/nearest/?x-api-key=" + APIKEY
        else:
            URL = f"https://api.checkwx.com/{type}/{icao}?x-api-key=" + APIKEY
        
        response = requests.get(URL)
        if response.status_code == 200: #200 = OK
            data = response.json()
            if data.get('results') == 1:
                return data
            return None
        
    def format_country_field(self, station: Station) -> str:
        """Format the embed country field with flag emoji and name"""
        if station.country_code:
            flag_emoji = f":flag_{station.country_code.lower()}:"
            return f"{flag_emoji} {station.country_name}"
        return station.country_name or "Unknown Country"

    def build_embed(self, 
                station: Station, metar: Metar, nearest) -> discord.Embed:
        embed = discord.Embed(
            title=f"{station.icao} METAR",
            description=f"{ "`NEAREST WX STATION METAR.`" if nearest else "\n" }\n\nLatest report is __{metar.age} minutes old__.\n```\n{metar.report}\n\n```",
            colour=0x00ff40,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Name", value=station.name or "N/A", inline=True)
        embed.add_field(name="Country", value=self.format_country_field(station), inline=True)
        embed.add_field(name="Elevation", value=f"{station.elevation_feet} ft" or "N/A", inline=True)
        
        embed.set_thumbnail(url="https://dmark.dev/public_assets/operational.jpg" if station.status == "Operational" else "https://dmark.dev/public_assets/uknown.jpg")
        embed.set_footer(text="Data provided by CheckWX", icon_url="")

        return embed
    
