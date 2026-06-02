from bs4 import BeautifulSoup
import requests

url = 'https://en.uesp.net/wiki/Morrowind:Alchemy_Effects'
response = requests.get(url)

PotionTypes = []
PotionArrays = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    threeRowsOfData = soup.find('table').tbody.tr.find_all('td', recursive=False)
    for row in threeRowsOfData:
        dataRows = row.table.tbody.find_all('tr', recursive=False)
        for data in dataRows:
            title_Ing = data.find_all('td', recursive=False)
            if len(title_Ing) > 1:
                titleBox = title_Ing[0].find_all('a', recursive=False)
                if len(titleBox) > 1:
                    PotionTypes.append(titleBox[1].get_text())
                ingredientsBoxs = title_Ing[1].ul.find_all('li')
                ingredients = []
                for box in ingredientsBoxs:
                    ingredients.append(box.a.get_text())
                PotionArrays.append(ingredients)
    print("{")
    for i, potType in enumerate(PotionTypes):
        print('	"' + potType + '": ["' + '", "'.join(PotionArrays[i]) + '"],')
    print("}")    
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

