import requests
from bs4 import BeautifulSoup
import lxml

url = 'https://aurora.edu'

# Get the page
page = requests.get(url)

# Create a BeautifulSoup object (navigable tree structure) using the lxml parser
soup = BeautifulSoup(page.text, 'lxml')

# Extract the title of the page
page_title = soup.title.string

# Print the title
print(page_title)