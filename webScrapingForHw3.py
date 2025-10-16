from bs4 import BeautifulSoup
import lxml
import requests

# URL of the webpage to scrape
url = 'https://editorial.rottentomatoes.com/guide/best-horror-movies-of-all-time/'

# Fetch the content from the URL
response = requests.get(url)

moviesData = []
directorsData = []
directedByData = []

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)

    # Find all books and their prices
    # row countdown-item
    movies = soup.find_all('div', class_='row countdown-item')
    books = soup.find_all('div', class_='article_movie_title')

    # Loop through each book and extract the title and price
    for i, movie in enumerate(movies):
        subsection = movie.find('div', class_='article_movie_title')
        title = subsection.h2.a.get_text()
        year = subsection.h2.span.get_text().replace('(', '').replace(')', '')
        movieLink = subsection.h2.a['href']
        rating = subsection.find('span', class_='tMeterScore').get_text().replace('%', '')
        
        link = movie.find('div', class_='info director')
        directors = link.find_all('a')
        text = ''
        for director in directors:
            text += director['href'] + " "
        
        moviesData.append([i, title, year, rating, "", ""])
        print(f"Movie {i + 1}: {title} - Year: {year} - Rating: {rating} - Link: {text}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

print("INSERT INTO movies (movieId, name, releaseYear, rating, runTime, boxOffice) VALUES")
print(f"({moviesData[0][0]}, '{moviesData[0][1]}', {moviesData[0][2]}, {moviesData[0][3]}, '{moviesData[0][4]}', {moviesData[0][5]},")
#(1, 'testMov', 2000, 74, '1h 44m', 286.5);


print("INSERT INTO directors (directorId, name, month, day, birthYear, favoriteColor) VALUES")
#(1, 'testDir', 'Jan', 12, 2006, 'Aquamarine');

print("INSERT INTO directedBy (movieId, directorId) VALUES")
#(1, 1);