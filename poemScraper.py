import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urljoin

# Citation: we looked this tutorial to get started with the BeautifulSoup library:
# http://brianabelson.com/open-news/2013/12/17/scrape-the-gibson.html

BASE_URL = 'http://www.poetryfoundation.org'

def scrape_poems():
    response = requests.get(BASE_URL + "/bio/edna-st-vincent-millay")
    soup = BeautifulSoup(response.content)
    poems = soup.find_all('a', {'class': 'title'})

    outputFile = open('edna-st-vincent-millay.txt', 'w')

    alreadyLoaded = set()

    for poem in poems:
        link = poem.attrs['href']
        if "poem" in link and link not in alreadyLoaded:
            url = urljoin(BASE_URL, link)
            scrape_poem(url, outputFile)
            alreadyLoaded.add(link)

    outputFile.close()

def scrape_poem(url, outputFile):
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    text = soup.find('div', {'class':'poem'}).text.strip()
    pprint(text)
    outputFile.write(text.encode("utf-8"))
    outputFile.write('\n#END#\n')

if __name__ == '__main__':
    scrape_poems()