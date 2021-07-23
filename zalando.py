#!/usr/bin/env python3
import json
from json.decoder import JSONDecoder
import requests
from bs4 import BeautifulSoup
from os import link
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent
from discord.ext import commands
from dotenv import load_dotenv
from urllib.parse import urlunsplit, urlencode
import requests as rq
import time
import json
import logging
import dotenv
import urllib3
from datetime import datetime, timedelta
from requests_html import HTMLSession


"""
logs
"""
logging.basicConfig(filename='MonitoLog.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s',
                    level=logging.DEBUG)
"""
configurations
"""
hardware_type = [HardwareType.MOBILE__PHONE]
software_names = [SoftwareName.CHROME.value]

user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)
CONFIG = dotenv.dotenv_values()

url="https://www.zalando.fr/nike-sportswear-dunk-baskets-basses-yellow-strikewhite-ni111a0y9-e11.html"
contentstring = "le contenu attendu"

headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
"Accept-Encoding": "gzip, deflate", 
"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
"Dnt": "1", 
"Host": "www.zalando.fr", 
"Upgrade-Insecure-Requests": "1", 
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36", 
"X-Amzn-Trace-Id": "Root=1-5ee7bae0-82260c065baf5ad7f0b3a3e3"
}


def scrape_site(url, headers,contentstring):
        test = requests.get(url, headers=headers).text
        soup = BeautifulSoup(test, 'html.parser')
        json_data = soup.find_all('script', id='z-vegas-pdp-props')
        print(test)
        for content in json_data:  
            contentstring = content.string 
    
        finalcontentstring = contentstring.strip()[9:-3].replace('449,00\xa0zł','hello')
        
        json_without_slash = json.loads(finalcontentstring)
        desired_data = json_without_slash['model']['articleInfo']
        
        
        globalid = desired_data['id']
        releasedate = desired_data['release_date']
        
        if releasedate is None:
            releasedate = "Already dropped"
        else:
            essaie = datetime.strptime(releasedate, "%y-%m-%d %I:%M:%S")
            convertedReleaseDate = essaie + timedelta(hours=2)
            convertedReleaseDate = convertedReleaseDate.strftime("%d-%m-%y %I:%M:%S")
            releasedate = convertedReleaseDate
        
        desired_data_units = desired_data['units']
        
        basics = []
        imagebasics = []
        fieldsSizes = []
        available_sizes = []
        available_pids = []
        available_stocks = []
        items = []

        for essential in [desired_data]:
            essentialsInfos = {
                'id': essential["id"], 
                'name': essential["name"],
                'shopUrl': essential['shopUrl'],
                }
        basics.append(essentialsInfos)
        
        
        mainimage = soup.find('img',{'class':'_6uf91T z-oVg8 u-6V88 ka2E9k uMhVZi FxZV-M _2Pvyxl JT3_zV EKabf7 mo6ZnF _1RurXL mo6ZnF PZ5eVw'})
        exelink = mainimage.attrs['src']

        for zalmainimage in [mainimage]:
            exelinkInfos = {
                'src': zalmainimage["src"], 
            }
        imagebasics.append(exelinkInfos)
        
        for units in desired_data['units']:
                        productitem = {
                            'pids': units["id"], 
                            'sizes': units['size']['local'], 
                            'stocks': units['stock'],
                            }
                        items.append(productitem)
                        
        
        newdict={}
        for k,v in [(key,d[key]) for d in items for key in d]:
            if k not in newdict: newdict[k]=[v]
            else: newdict[k].append(v)
            
        for pids in newdict['pids']:
                available_pids.append(pids),
                
        allPids = '\n'.join(available_pids) 
            
        for size in newdict['sizes']:
                available_sizes.append(size),
                
        allSizes = '\n'.join(available_sizes) 
        
        for stocks in newdict['stocks']:
                available_stocks.append(stocks),
        
        '''
        available_stocks_toString int to string stock for the embed
        '''       
        available_stocks_toString = [str(int) for int in available_stocks]
        str_of_ints = "\n".join(available_stocks_toString)
        
        total_stock = sum(available_stocks)
        total_stock_to_string = str(total_stock)

        fieldsSizes.append({"name":"GLOBAL ID", "value":globalid, "inline": True})
        fieldsSizes.append({"name":"TOTAL STOCK", "value":total_stock_to_string, "inline": True})
        fieldsSizes.append({"name":"RELEASE DATE", "value":releasedate, "inline": True})
        fieldsSizes.append({"name":"SIZES", "value":allSizes, "inline": True})
        fieldsSizes.append({"name":"SIZE PIDS", "value":allPids, "inline": True})
        fieldsSizes.append({"name":"STOCK", "value":str_of_ints, "inline": True})
        
        data = {
            "username": CONFIG['USERNAMEZAL'],
            "avatar_url": CONFIG['AVATAR_URL'],
            "embeds": [{
                "author": {
                "name": "Izi Cookz", 
                "icon_url": CONFIG['AVATAR_URL'],
                },
                "title": essential["name"],
                "thumbnail": {"url": exelink},
                "fields": fieldsSizes,
                "color": int(CONFIG['COLOUR']),
                "footer": {"text": "Made by JLM for Izi Cookz","icon_url": "https://media1.tenor.com/images/bcebfc84143c63f127c7fd80826f01bf/tenor.gif?itemid=22297787"},
                "timestamp": str(datetime.utcnow()),
                "url": essential['shopUrl'],
            }]
        }
        result = rq.post(CONFIG['WEBHOOKZAL'], data=json.dumps(data), headers={"Content-Type": "application/json"})
    
  

   
def discordbot():
    bot = commands.Bot(command_prefix="!")
    TOKEN = CONFIG['DISCORD_TOKEN']

    @bot.event
    async def on_ready():
        print(f'Bot connected as {bot.user}')
        
    @bot.command("zalando")
    async def dosomething(ctx,url):
        scrape_site(url, headers, contentstring)
           


    bot.run(TOKEN)

if __name__ == '__main__':
  discordbot()

  

 
