import ashkeebsStock
import bolsaStock
import logging
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

### This is the main python file for calling 2 scripts to check keyboard switch stocks on bolsasupply.com and ashkeebs.com

logname = 'switchstock.log'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running switch stock script")
logger = logging.getLogger('switchstockscraper')

with open(r"switchstock.log", 'r') as fp:
    for count, line in enumerate(fp):
        pass

count_num = count + 1
print(count_num)
# Define the registry
registry = CollectorRegistry()
g = Gauge('Switch_Stock_Logger_Count', 'counts web scraper logs', registry=registry)
g.set(count_num)
push_to_gateway('prometheus.local:9091', job='switch_stock_logs', registry=registry)
