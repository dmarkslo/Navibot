from datetime import datetime, timezone
from ..command import Command 
import requests
import discord
from math import floor
import pandas as pd



#COMMAND IS STILL NOT FINISHED, WIP

class AtcCommand(Command):

    def __init__(self):
        super().__init__(name="atc",description="Displays VATSIM ATC stations and their frequencies for ICAO.")
        self.syntax = f"${self.name} ICAO"

    async def execute(self, ctx, *args):
        icao = args[0]
        online_atc = self.fetch_data_from_api(icao)
        await ctx.reply(embed=self.build_embed(icao,online_atc))
        
    def fetch_data_from_api(self, icao):
        #   First stage, inefficient loop through list to check if callsign = icao and print.
        #   Think of a way to sort json and use efficient search, especially so i wont have 
        #   to check double conditions for each one that doesnt start with icao.
        URL = f"https://api.vatsim.net/v2/atc/online"

        payload={}
        headers = {
        'Accept': 'application/json'
        }

        response = requests.request("GET", URL, headers=headers, data=payload)
        
        if response.status_code == 200: #200 = OK
            atc = {}
            data = response.json()
            usa_icao = icao[1:]
            for atc_position in data:
                if atc_position['callsign'].startswith(icao) or atc_position['callsign'].startswith(usa_icao):
                    atc[atc_position['callsign']] = atc_position['start']
            return atc
        else:
            # TODO: Throw errors/notify user for API error codes
            return {} 

    def atc_time_online(self,timestamp_string):
        atc_start_utc_datetime = datetime.fromisoformat(timestamp_string)
        curr_utc_datetime = datetime.now(timezone.utc)  
        return floor((curr_utc_datetime - atc_start_utc_datetime).total_seconds() / 60)

    def build_embed(self,icao, data) -> discord.Embed:
        embed = discord.Embed(
            title="",
            description=f"{ f"No ATC online at {icao}." if not data else "\n" }\n",
            colour=0x00ff40 if data else 0x800000,
            timestamp=datetime.now()
        )

        
        
        if data:
            embed.add_field(name=f"ATC online at {icao}", value=f"", inline=False)
            for key in data:
                embed.add_field(name=f"`{key}`", value=f"online for {self.atc_time_online(data[key])} min." or "N/A", inline=False)
         
        embed.set_footer(text="Data provided by VATSIM", icon_url="https://vatsim.dev/img/logo.png")

        return embed
    
