import json
import requests
from bs4 import BeautifulSoup
from os import link
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent
import discord
from dotenv import load_dotenv
from urllib.parse import urlunsplit, urlencode
import requests as rq
import time
import json
import logging
import dotenv
import urllib3
from datetime import datetime
import discord
from dotenv import load_dotenv
import random 

load_dotenv()

CONFIG = dotenv.dotenv_values()

load_dotenv()
TOKEN = CONFIG['DISCORD_TOKEN']

client = discord.Client()

@client.event
async def on_message(message):

