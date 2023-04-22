import requests
from bs4 import BeautifulSoup
import discord
import re
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

ashkeebs = 'https://www.ashkeebs.com/product/zaku-ii-tactile-switches/'
webhookurl = 'https://discord.com/api/webhooks/' ## Discord Webhook

dataStock = {
    "content" : "**Switch Stock Status - Ashkeebs** <@DiscordID>",
    "username" : "Switch Stock Alert"
}

dataStock["embeds"] = [
    {
        "description" : "Zaku v2 Switch In Stock: https://www.ashkeebs.com/product/zaku-ii-tactile-switches/",
        "title" : "Switch in Stock!!",
        "color": "14177041"
    }
]

dataStatus = {
    "content" : "**Switch Status Code DOWN - Ashkeebs** <@DiscordID>",
    "username" : "Switch Stock Alert"
}

dataStatus["embeds"] = [
    {
        "description" : "Something is Wrong with URL!: https://www.ashkeebs.com/product/zaku-ii-tactile-switches/",
        "title" : "Status Code Not 200!",
        "color": "15548997"
    }
]

def ashkeebsStatCode():
    ashkeebsStatus = requests.request('GET', ashkeebs)
    if ashkeebsStatus.status_code != 200:
        result = requests.post(webhookurl, json = dataStatus)
        result
    else:
        ashRegistry = CollectorRegistry()
        ashGauge = Gauge('AshStatusCode', 'status code of ashkeebs', registry=ashRegistry)
        statusCode = str(ashkeebsStatus.status_code)
        ashGauge.set(statusCode)
        push_to_gateway('prometheushost.local:9091', job='web_status', registry=ashRegistry)
ashkeebsStatCode()

def ashkeebsFun():
    ashkeebsweb = requests.request('GET', ashkeebs)
    soup = BeautifulSoup(ashkeebsweb.text, 'html.parser')
    div_p = soup.find("div", {"class":"fusion-woo-cart fusion-woo-cart-1"})
    divparse = div_p.text
    divRe = re.match("(?:Out\s)", divparse)
    if re.match("(?:Out\sof)", divparse):
        None
    else:
        result = requests.post(webhookurl, json = dataStock)
        result
        print('IN STOCK BUY NOW, website: https://www.ashkeebs.com/product/zaku-ii-tactile-switches/')
ashkeebsFun()
