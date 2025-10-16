import requests
from bs4 import BeautifulSoup
import lxml
# This code will webscrape for course number, course name and course
# description of courses from the CSC program requirements page at AU.
# The majority of this code was modified from external sources, including ChatGPT.
# NOTE *** This code uses verify=False which will ignore any SSL certification
# checks. This is problematic and should be used with caution.

def fetch_course_description(url):
    try:
        # Request the data in the popup window for the course description
        response = requests.post(url, verify=False)
        # remove verify=false on normal websites because it could be a bogus website

        # Parse the response as HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'lxml')
        # Find the first <p> tag with the class 'courseblockextra noindent'
        description_tag = soup.find('div', class_='courseblockextra noindent')

        if description_tag:
            # Extract and clean the text content from the tag
            description = description_tag.get_text(strip=True)
            return description
        else:
            return "Description not found."

    except requests.RequestException as e:
        return f"Failed to retrieve course description: {e}"


url = 'https://catalog.aurora.edu/undergraduate/programs/computer-science/#programrequirementstext'

# Get the page with course requirements for CSC and store in page as raw HTML
page = requests.get(url, verify=False)
# remove verify=false on normal websites because it could be a bogus website
# only do it when it is safe to go into it.

# Create a BeautifulSoup object (navigable tree structure) using the lxml parser
soup = BeautifulSoup(page.text, 'lxml')

# Create a list of rows that follow tbody tr
course_rows = soup.select('tbody tr')

# Loop through the rows to find course information
for row in course_rows:
    code_col = row.find('td', class_='codecol')
    # If td is found in class 'codecol' then the td must also have an <a> tag
    if code_col and code_col.a:
        # Extract data from the td information
        tds = row.find_all('td')

        #print (tds[0])#uncomment to see what this looks like
        course_number = tds[0].a['title']
        # Get the title from the second <td>
        # print (tds[1]) - uncomment to see what this looks like
        course_title = tds[1].text.strip()

        # to get the course description requires finding the html that
        # corresponds to the pop up window
        # Construct course URL - How did I find this URL?
        course_url = f'https://catalog.aurora.edu/ribbit/index.cgi?page=getcourse.rjs&code={course_number}'
        course_description = fetch_course_description(course_url)

        # Print the course information
        print(f"Course Number: {course_number}")
        print(f"Course Title: {course_title}")
        print(f"URL: {course_url}")
        print(f"Description: {course_description}")
        print("-" * 40)