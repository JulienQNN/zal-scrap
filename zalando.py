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


url = 'https://www.zalando.fr/jordan-air-1-baskets-basses-gym-redwhiteblack-joc11a020-g12.html'
headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}

def scrape_site(url, headers):
    
    itemsbasic= []
    s = rq.Session()
    soup = BeautifulSoup(s.get(url, headers=headers).content, 'html.parser')

    json_data = json.loads(soup.select_one('#z-vegas-pdp-props').contents[0].replace('<![CDATA[', '').replace(']]>', ''))

    desired_data = dict(json_data['model']['articleInfo'])
    json_output = json.dumps(desired_data)
    essentials = json.loads(json_output)

    basics = []
    items = []

    for essential in [essentials]:
        essentialsInfos = {
            'globalid': essential["id"], 
            'name': essential["name"],
            'link': essential['shopUrl'],
            }
    basics.append(essentialsInfos)

    mainimage = soup.find('img',{'class':'_6uf91T z-oVg8 u-6V88 ka2E9k uMhVZi FxZV-M _2Pvyxl JT3_zV EKabf7 mo6ZnF _1RurXL mo6ZnF PZ5eVw'})
    exelink = mainimage.attrs['src']

    for zalmainimage in [mainimage]:
        exelinkInfos = {
            'src': zalmainimage["src"], 
        }
    basics.append(exelinkInfos)
                
    for units in essentials['units']:
                    productitem = {
                        'pids': units["id"], 
                        'sizes': units['size']['local'], 
                        'stocks': units['stock'],
                        }
                    items.append(productitem)
    s.close()
    itemsbasic = basics + items
    print(itemsbasic)
 
    
    essential_item = [essential['id'], essential['name'], essential['shopUrl']]
    units_item = [units['id'], units['size']['local'], units['stock']]   
     
          
    name = []
    globalid = []
    fieldsSizes = []
    listeSizes = []
    listePids = []
    listeStocks = []
    
    totalStocks = sum(listeStocks)
    
    for shopUrl in essential_item:
        listeStocks.append(shopUrl),
    stocksscraped = '\n'.join(listeStocks) 
    
    for name in essential['name']:
        listeStocks.append(name),
    stocksscraped = '\n'.join(listeStocks) 
    
    for globalid in essential['id']:
        listeStocks.append(globalid),
    stocksscraped = '\n'.join(listeStocks) 
    
    
    for size in units['size']['local']:
        listeSizes.append(size),
    sizesscraped = '\n'.join(listeSizes) 
    
    for pid in units['id']:
        listePids.append(pid),
    pidsscraped = '\n'.join(listePids) 
    
    for stock in units['stock']:
        listeStocks.append(stock),
    stocksscraped = '\n'.join(listeStocks) 
    
    
    print(fieldsSizes)
    fieldsSizes.append({"name":globalid, "value":"\u200b", "inline": False})
    fieldsSizes.append({"name":name, "value":"\u200b", "inline": False})
    fieldsSizes.append({"name":"TOTAL STOCK", "value":totalStocks, "inline": False})
    fieldsSizes.append({"name":"PIDS", "value":sizesscraped, "inline": False}),
    fieldsSizes.append({"name":"SIZES", "value":pidsscraped, "inline": False}),
    fieldsSizes.append({"name":"STOCK", "value":stocksscraped, "inline": False}),
    fieldsSizes.append({"name":"FR", "value":link, "inline": False}),
    
    data = {
        "username": CONFIG['USERNAME'],
        "avatar_url": CONFIG['AVATAR_URL'],
        "embeds": [{
            "author": {
            "name": "Izi Zalando Scraper", 
            "url": "https://dashboard.izicookz.com/",
            "icon_url": CONFIG['AVATAR_URL'],
            },
            "title": name,
            "thumbnail": {"url": shopUrl},
            "color": int(CONFIG['COLOUR']),
            "fields": fieldsSizes,
            "url": link,
            "footer": {"text": "Made by JLM for Izi Cookz","icon_url": "https://media1.tenor.com/images/bcebfc84143c63f127c7fd80826f01bf/tenor.gif?itemid=22297787"},
            "timestamp": str(datetime.utcnow()),
        }]
    }
    
    result = rq.post(CONFIG['WEBHOOK'], data=json.dumps(data), headers={"Content-Type": "application/json"})
    result


def test_webhook():
    data = {
        "username": CONFIG['USERNAME'],
        "avatar_url": CONFIG['AVATAR_URL'],
        "embeds": [{
            "title": "Testing Webhook",
            "description": "This is just a quick test to ensure the webhook works. Thanks again for using these monitors!",
            "color": int(CONFIG['COLOUR']),
            "footer": {'text': 'Made by Yasser'},
            "timestamp": str(datetime.utcnow())
        }]
    }

    result = rq.post(CONFIG['WEBHOOK'], data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except rq.exceptions.HTTPError as err:
        logging.error(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))
        logging.info(msg="Payload delivered successfully, code {}.".format(result.status_code))

scrape_site(url, headers)

'''
def monitor():
    
    test = scrape_site(url, headers)
    for p in test:
        comparitor(p, start)
    """
    Initiates the monitor
    """
    print('STARTING MONITOR')
    logging.info(msg='Successfully started monitor')
    # Tests webhook URL
    test_webhook()
    discord_webhook(
                    name=essentialsInfos['name'],
                    url="https://wtb.wethenew.com/",
                    thumbnail=product['image'],
                    sizes=available_sizes
                )


if __name__ == "__main__":
    # execute only if run as a script

    monitor()
    
  #  botresponse()
  '''



 