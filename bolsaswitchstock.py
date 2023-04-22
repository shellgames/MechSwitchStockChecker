import requests
from bs4 import BeautifulSoup
import discord
import re
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


bolsa = 'https://bolsakeyboardsupply.com/collections/switches/products/zaku-ii-switch'
webhookurl = 'https://discord.com/api/webhooks' ## Add discord webhook info here

dataStock = {
    "content" : "**Switch Stock Status - Bolsa Supply** <@DiscordID#>",
    "username" : "Switch Stock Alert"
}

dataStock["embeds"] = [
    {
        "description" : "Zaku v2 Switch In Stock: https://bolsakeyboardsupply.com/collections/switches/products/zaku-ii-switch",
        "title" : "Switch in Stock!!",
        "color": "14177041"
    }
]

dataStatus = {
    "content" : "**Switch Status Code DOWN - Bolsa Supply** <@DiscordID#>",
    "username" : "Switch Stock Alert"
}

dataStatus["embeds"] = [
    {
        "description" : "URL not Working: https://bolsakeyboardsupply.com/collections/switches/products/zaku-ii-switch",
        "title" : "Status Code NOT 200!",
        "color": "15548997"
    }
]

def bolsaStatCode():
    bolsaStatus = requests.request('GET', bolsa)
    if bolsaStatus.status_code != 200:
        result = requests.post(webhookurl, json = dataStatus)
        result
    else:
        bolsaRegistry = CollectorRegistry()
        bolsaGauge = Gauge('BolsaStatusCode', 'status code of bolsa supply', registry=bolsaRegistry)
        statusCode = str(bolsaStatus.status_code)
        bolsaGauge.set(statusCode)
        push_to_gateway('prometheushost.local:9091', job='web_status', registry=bolsaRegistry)
bolsaStatCode()

def bolsasupplyFun():
    bolsaweb = requests.request('GET', bolsa)
    soup = BeautifulSoup(bolsaweb.text, 'html.parser')
    div_p = soup.find("button", {"id":"addToCart-product-template"})
    divtxt = div_p.text[9:20]
    if re.match("(Unava)", divtxt):
        None
    else:
        result = requests.post(webhookurl, json = dataStock)
        result
        print('IN STOCK BUY NOW, website: https://bolsakeyboardsupply.com/collections/switches/products/zaku-ii-switch')
bolsasupplyFun()
