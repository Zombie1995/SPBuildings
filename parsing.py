import lxml
import requests
from bs4 import BeautifulSoup
url_1 = 'https://www.citywalls.ru/'
url_2 = 'https://www.citywalls.ru/sights-city1.html'
response = requests.get(url_2)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('td')
with open('citywalls.html') as file:
    file.write(quotes)

