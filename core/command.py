from __future__ import annotations
from typing import Optional
from discord.ext import commands
from .station import Station
from .metar import Metar
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
            station = self.fetch_station(args[0])
            if station:
                metar = self.fetch_metar(args[0])
                embed = self.build_embed(station, metar)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Oops! An error has occured. Please check ICAO input is valid.")             

    def fetch_station(self,icao: str):
        """Fetch station (aka airport) data from url"""
        url = f"https://api.checkwx.com/station/{icao}?x-api-key=" + APIKEY
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('results') == 1:
                return Station(data)
            return None
    
    def fetch_metar(self,icao: str):
        """Fetch metar data from url"""
        url = f"https://api.checkwx.com/metar/{icao}?x-api-key="+ APIKEY
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if response.json()['results'] == 1:
                return Metar(data)
            return None
    
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
        embed.add_field(name="Elevation", value=f"{station.elevation_feet} (ft)" or "N/A", inline=True)
        embed.add_field(name="Status", value=station.status or "N/A", inline=True)
        
        embed.set_thumbnail(url="https://dmark.dev/public_assets/operational.jpg" if station.status == "Operational" else "https://dmark.dev/public_assets/uknown.jpg")
        embed.set_footer(text="Data provided by CheckWX", icon_url="")

        return embed

    
                    

class CmdsCommand(Command):

    def __init__(self):
        super().__init__(name="cmds",description="Displays all valid commands for NaviBot.")

    async def execute(self, ctx, *args):
        await ctx.send("$metar : Displays a weather METAR report for valid airport ICAO.\n$cmds : Displays all valid commands for NaviBot.")
        
            




