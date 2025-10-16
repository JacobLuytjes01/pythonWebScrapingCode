from bs4 import BeautifulSoup
import lxml
import requests
import re

def fetch_director(url):
    returnBlock = ["NULL", "NULL", "NULL", "NULL"]
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup)
            returnBlock[0] = soup.find('h1', class_='celebrity-bio__h1').get_text()
            bioData = soup.find_all('p', class_='celebrity-bio__item')
            birthdate = bioData[2].getText().splitlines()[2].strip().split(' ')
            print(bioData)
            returnBlock[1] = birthdate[0]
            returnBlock[2] = birthdate[1]
            returnBlock[3] = birthdate[2]
            
        return returnBlock
    except requests.RequestException as e:
        return returnBlock

def fetch_movie_data(url):
    returnBlock = ["NULL", "NULL"]
    return returnBlock
    try:
        if response.status_code == 200:
            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup)
            year = soup.find('section', class_='media-info').find('div', class_='content-wrap').find_all('rt-text', attrs={"data-qa" : "item-value"})
    
            x = re.findall(">[0-9]+h [0-9]+m<", str(year))
            if x:
                returnBlock[0] = x[0].replace(">", "").replace("<", "")
    
            y = re.findall(">[A-Z][a-z][a-z] [0-9]+, [1-2][0-9][0-9][0-9]", str(year))
            if y:
                returnBlock[1] = y[0].replace(">", "")
        
            return returnBlock
    except requests.RequestException as e:
        return returnBlock


# URL of the webpage to scrape
url = 'https://editorial.rottentomatoes.com/guide/best-horror-movies-of-all-time/'
# Fetch the content from the URL
response = requests.get(url)

moviesData = []
directorsData = []
directedByData = []
directorsId = 1;

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)

    # Find all books and their prices
    # row countdown-item
    movies = soup.find_all('div', class_='row countdown-item')

    # Loop through each book and extract the title and price
    for i, movie in enumerate(movies):
        subsection = movie.find('div', class_='article_movie_title')
        title = subsection.h2.a.get_text()
        year = subsection.h2.span.get_text().replace('(', '').replace(')', '')
        #movieLink = subsection.h2.a['href']
        print(subsection.h2.a['href'])
        movieData = fetch_movie_data(subsection.h2.a['href'])
            
        
        rating = subsection.find('span', class_='tMeterScore').get_text().replace('%', '')
        
        link = movie.find('div', class_='info director')
        directors = link.find_all('a')
        text = ''
        for director in directors:
            print("https:" + director['href'])
            directorData = fetch_director(director['href'])
            directorsData.append([directorsId, directorData[0], directorData[1], directorData[2], directorData[3]])
            directedByData.append([i+1, directorsId])
            directorsId += 1
        
        moviesData.append([i+1, title, year, rating, movieData[0], movieData[1]])
        #print(f"Movie {i + 1}: {title} - Year: {year} - Rating: {rating} - Link: {text}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

print("INSERT INTO movies (movieId, name, releaseYear, rating, runTime, boxOffice) VALUES")
sliced_list = moviesData[:-1]
for singleMovie in sliced_list:
            print(f"({singleMovie[0]}, '{singleMovie[1]}', {singleMovie[2]}, {singleMovie[3]}, '{singleMovie[4]}', {singleMovie[5]}),")
print(f"({moviesData[-1][0]}, '{moviesData[-1][1]}', {moviesData[-1][2]}, {moviesData[-1][3]}, '{moviesData[-1][4]}', {moviesData[-1][5]});")

#print(f"({moviesData[0][0]}, '{moviesData[0][1]}', {moviesData[0][2]}, {moviesData[0][3]}, '{moviesData[0][4]}', {moviesData[0][5]},")
#(1, 'testMov', 2000, 74, '1h 44m', 286.5);


print("INSERT INTO directors (directorId, name, month, day, birthYear, favoriteColor) VALUES")
sliced_list = directorsData[:-1]
for singleDirector in sliced_list:
            print(f"({singleDirector[0]}, '{singleDirector[1]}', {singleDirector[2]}, {singleDirector[3]}, '{singleDirector[4]}', NULL),")
print(f"({directorsData[-1][0]}, '{directorsData[-1][1]}', {directorsData[-1][2]}, {directorsData[-1][3]}, '{directorsData[-1][4]}', NULL);")
#(1, 'testDir', 'Jan', 12, 2006, 'Aquamarine');

print("INSERT INTO directedBy (movieId, directorId) VALUES")
sliced_list = directedByData[:-1]
for direct in sliced_list:
            print(f"({direct[0]}, '{direct[1]}'),")
print(f"({directedByData[-1][0]}, '{directedByData[-1][1]}');")
#(1, 1);
