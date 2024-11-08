from __future__ import annotations
from discord.ext import commands
from .Station import Station
from .Metar import Metar
from datetime import datetime
from config import APIKEY
import requests
import discord



class Command():

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    async def execute(self):
        """Execute command. (Abstract method) """
        pass



class MetarCommand(Command):

    def __init__(self):
        super().__init__(name="metar",description="Displays a weather METAR report for valid airport ICAO.")

    async def execute(self, ctx, *args):
        if args:
            station_data = self.fetch_data_from_api("station",args[0])
            if station_data:
                metar_data = self.fetch_data_from_api("metar",args[0])
                await ctx.send(embed=self.embed_data(station_data,metar_data))
            else:
                await ctx.send("Oops! An error has occured. Please check ICAO input is valid.")             


    def fetch_data_from_api(self, type, icao):
        url = f"https://api.checkwx.com/{type}/{icao}?x-api-key=" + APIKEY
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('results') == 1:
                return data
            return None
        
    def embed_data(self, station_data, metar_data):
        return self.build_embed(Station(station_data), Metar(metar_data))

    def get_country_field(self, station: Station) -> str:
        """Format the country field with flag emoji and name"""
        if station.country_code:
            flag_emoji = f":flag_{station.country_code.lower()}:"
            return f"{flag_emoji} {station.country_name}"
        return station.country_name or "Unknown Country"

    def build_embed(self, station: Station, metar: Metar) -> discord.Embed:
        embed = discord.Embed(
            title=f"{station.icao} METAR",
            description=f"\nLatest report:\n```\n{metar.value}\n\n```",
            colour=0x00b0f4,
            timestamp=datetime.now()
        )
        embed.set_author(name="NaviBot - METAR Request")
        
        embed.add_field(name="Name", value=station.name or "N/A", inline=True)
        embed.add_field(name="City", value=station.city or "N/A", inline=True)
        embed.add_field(name="Country", value=self.get_country_field(station), inline=True)
        embed.add_field(name="Elevation", value=f"{station.elevation_feet} ft" or "N/A", inline=True)
        
        embed.set_thumbnail(url="https://dmark.dev/public_assets/operational.jpg" if station.status == "Operational" else "https://dmark.dev/public_assets/uknown.jpg")
        embed.set_footer(text="Data provided by CheckWX", icon_url="")

        return embed

    
                    

class CmdsCommand(Command):

    def __init__(self):
        super().__init__(name="cmds",description="Displays all valid commands for NaviBot.")

    async def execute(self, ctx, *args):
        await ctx.send("$metar : Displays a weather METAR report for valid airport ICAO.\n$cmds : Displays all valid commands for NaviBot.")
        
            




