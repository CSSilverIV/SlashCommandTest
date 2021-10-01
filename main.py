import os
import discord
import urllib.request
import urllib
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option #needed to make choices and options; unused for now
from bs4 import BeautifulSoup
import tabulate

#Setting up the bot
client=commands.Bot(command_prefix="!")
slash=SlashCommand(client,sync_commands=True)
bot_token = os.getenv('bot_token_2')

#Function to get table by web scrapping once the slash comand has been called
def getTable():
  tableurl="https://www.skysports.com/premier-league-table"
  page=urllib.request.urlopen(tableurl).read()
  pagesoup = BeautifulSoup(page, 'html.parser')
  tablemain=pagesoup.find('table',{'class':'standing-table__table'})

  headers=tablemain.find('thead')
  data=[]
  
  #Gets table headers
  cols = headers.find_all('th')
  cols = [ele.text.strip() for ele in cols]
  cols.pop()
  data.append([ele for ele in cols if ele]) # Get rid of empty values

  #Gets table body
  tablebody=tablemain.find('tbody')
  rows = tablebody.find_all('tr')
  for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      data.append([ele for ele in cols if ele]) # Get rid of empty values

  print(data)
  return data #Returns table

#Setting up the slash command
@slash.slash(
  name="epltable", #Name of the command as you want it to appear on Discord
  description="Display EPL Table", #What it does

  #Options allows users to add arguments to the command or choices and buttons,
  #Unused for now

  # options=[
  #   create_option(
  #     name="lengthoftable",
  #     description="No of positions to be viewed",
  #     option_type=4,
  #     required=False
  #   )
  # ]
)

#Bot behaviour upon receiving a slash command
async def _tableEPL(ctx:SlashContext):
  table=tabulate.tabulate(getTable(),headers='firstrow',tablefmt='pretty')
  print(table)
  await ctx.send("```"+table+"```")

#Run bot!
client.run(bot_token)  

 