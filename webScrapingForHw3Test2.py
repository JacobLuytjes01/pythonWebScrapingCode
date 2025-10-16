from bs4 import BeautifulSoup
import lxml
import requests

# URL of the webpage to scrape
url = 'https://www.rottentomatoes.com/celebrity/steve_spielberg/'

# Fetch the content from the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    
    # Find all books and their prices
    # row countdown-item


    name = soup.find('h1', class_='celebrity-bio__h1').get_text()
    bioData = soup.find_all('p', class_='celebrity-bio__item')
    birthdate = bioData[2].getText().splitlines()[2].strip().split(' ')
    
    
    print(f"Director: {name} - Birthday: month: {birthdate[0]} day: {birthdate[1].replace(',', '')} Year: {birthdate[2]}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


