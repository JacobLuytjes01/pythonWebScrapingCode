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
            
            returnBlock[0] = soup.find('h1', class_='celebrity-bio__h1').get_text()
            bioData = soup.find_all('p', class_='celebrity-bio__item')
            birthdate = bioData[2].getText().splitlines()[2].strip().split(' ')
            
            returnBlock[1] = birthdate[0]
            if 1 < len(birthdate):
                returnBlock[2] = birthdate[1]
            if 2 < len(birthdate):
                returnBlock[3] = birthdate[2]
            
        return returnBlock
    except requests.RequestException as e:
        return returnBlock

def fetch_movie_data(url):
    returnBlock = ["NULL", "NULL"]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            dataBlock = soup.find('section', class_='media-info').find('div', class_='content-wrap').find_all('rt-text', attrs={"data-qa" : "item-value"})
            
            runTime = re.findall(">[0-9]+h [0-9]+m<", str(dataBlock))
            if runTime:
                returnBlock[0] = "'"+ runTime[0].replace(">", "").replace("<", "") + "'"
            else:
                runTime = re.findall(">[0-9]+m<", str(dataBlock))
                if runTime:
                    returnBlock[0] = "'"+ runTime[0].replace(">", "").replace("<", "") + "'"
                
            boxOffice = re.findall('\$[0-9]+.[0-9][KM]', str(dataBlock))
            if boxOffice:
                returnBlock[1] = float(boxOffice[0].replace('$', "")[:-1])
                if (boxOffice[0][-1] == 'K'):
                    returnBlock[1] = returnBlock[1] * 1000
                elif (boxOffice[0][-1] == 'M'):
                    returnBlock[1] = returnBlock[1] * 1000000
            else:
                returnBlock[1] = "NULL"
        
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
    movies = soup.find_all('div', class_='row countdown-item')

    for i, movie in enumerate(movies):
        subsection = movie.find('div', class_='article_movie_title')
        title = subsection.h2.a.get_text().replace("'", "''")
        year = subsection.h2.span.get_text().replace('(', '').replace(')', '')
        movieData = fetch_movie_data(subsection.h2.a['href'])
            
        
        rating = subsection.find('span', class_='tMeterScore').get_text().replace('%', '')
        
        link = movie.find('div', class_='info director')
        directors = link.find_all('a')
        for director in directors:
            directorData = fetch_director("https:" + director['href'])
            success = False;
            for director2 in directorsData:
                if(not success and director2[1] == directorData[0] and director2[2] == directorData[1] and director2[3] == directorData[2] and director2[4] == directorData[3]):
                    directedByData.append([i+1, director2[0]])
                    success = True
            
            if (not success):
                directorsData.append([directorsId, directorData[0], directorData[1], directorData[2], directorData[3]])
                directedByData.append([i+1, directorsId])
                directorsId += 1
        
        moviesData.append([i+1, title, year, rating, movieData[0], movieData[1]])
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

print("INSERT INTO movies (movieId, name, releaseYear, rating, runTime, boxOffice) VALUES")
sliced_list = moviesData[:-1]
for singleMovie in sliced_list:
    print(f"({singleMovie[0]}, '{singleMovie[1]}', {singleMovie[2]}, {singleMovie[3]}, {singleMovie[4]}, {singleMovie[5]}),")
print(f"({moviesData[-1][0]}, '{moviesData[-1][1]}', {moviesData[-1][2]}, {moviesData[-1][3]}, {moviesData[-1][4]}, {moviesData[-1][5]});")

print("INSERT INTO directors (directorId, name, month, day, birthYear, favoriteColor) VALUES")
sliced_list = directorsData[:-1]
for singleDirector in sliced_list:
    if (singleDirector[2] == "Not"):
        print(f"({singleDirector[0]}, '{singleDirector[1]}', NULL, NULL, NULL, NULL),")
    else:
        print(f"({singleDirector[0]}, '{singleDirector[1]}', '{singleDirector[2]}', {singleDirector[3]} {singleDirector[4]}, NULL),")
        
if (directorsData[-1][2] == "Not"):
    print(f"({directorsData[-1][0]}, '{directorsData[-1][1]}', NULL, NULL, NULL, NULL);")
else:
    print(f"({directorsData[-1][0]}, '{directorsData[-1][1]}', '{directorsData[-1][2]}', {directorsData[-1][3]} {directorsData[-1][4]}, NULL);")

print("INSERT INTO directedBy (movieId, directorId) VALUES")
sliced_list = directedByData[:-1]
for direct in sliced_list:
    print(f"({direct[0]}, {direct[1]}),")
print(f"({directedByData[-1][0]}, {directedByData[-1][1]});")
