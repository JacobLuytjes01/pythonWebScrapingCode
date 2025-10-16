from bs4 import BeautifulSoup
import lxml
import requests
import re

# URL of the webpage to scrape
test = "osdngkfdn>4h 3m<gndfkn"

x = re.findall(">[0-9]+h [0-9]+m<", test)
if x:
    print(f'{x}')


