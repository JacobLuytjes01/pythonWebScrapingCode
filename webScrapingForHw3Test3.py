from bs4 import BeautifulSoup
import lxml
import requests
import re

# URL of the webpage to scrape
url = 'https://www.rottentomatoes.com/m/jaws/'

# Fetch the content from the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    year = soup.find('section', class_='media-info').find('div', class_='content-wrap').find_all('rt-text', attrs={"data-qa" : "item-value"})
    
    x = re.findall(">[0-9]+h [0-9]+m<", str(year))
    if x:
        print(f'{x[0].replace(">", "").replace("<", "")}')
    
    y = re.findall(">[A-Z][a-z][a-z] [0-9]+, [1-2][0-9][0-9][0-9]", str(year))
    if y:
        print(f'{y[0].replace(">", "")}')
    
    #print(year)
    #for i, test in enumerate(year):
    #    x = re.findall(">[0-9]+h [0-9]+m<", str(test))
    #    if x:
    #        print(f'{i}, {x}')
    #    print(f'{i}, {test}')
        
        
    #print(year)
    
    #year = soup.find_all('dd')
    #print(year)
    #for i, test in enumerate(year):
            #print(f"{i}: {test}")
    
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")



