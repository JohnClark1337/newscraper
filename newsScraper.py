import requests
#import wget
import pdfkit
import os
import webbrowser
from arsScrape import arsScrape
from bs4 import BeautifulSoup
config = pdfkit.configuration(wkhtmltopdf="wkhtmltox/bin/wkhtmltopdf.exe")
originalPage = 'https://news.ycombinator.com/'
page = requests.get(originalPage)
soup = BeautifulSoup(page.content, 'lxml')
technica = arsScrape()

nextSite = ''

home = os.path.expanduser('~')
linkList = list()
nameList = list()

yesList = "YES, Y, ABSOLUTELY"
noList = "NO, N, NEGATIVE"


#hackerNews
def hackerNewsSearch():
    global soup
    end = False
    while end == False:
        empty = 0
        for item in soup.find_all('td', class_ = 'title'):
            try:
                if searchTerm.upper() in str(item.find('a', class_ ='storylink').text).upper():
                    nameList.append(item.find('a', class_ = 'storylink').text)
                    linkList.append(item.a['href'])
            except Exception as e:
                empty += 1
        try:
            nextSite = item.find('a', class_ = 'morelink')['href']
            page = requests.get(originalPage + nextSite)
            soup = BeautifulSoup(page.content, 'html.parser')
        except Exception as e:
            end = True





searchTerm = input("What would you like to search for? ")
print("Searching hackernews...")   
hackerNewsSearch()
print("Searching ArsTechnica...")
technica.runArsScrape()
linkList = linkList + technica.getLinks(searchTerm)
nameList = nameList + technica.getNames(searchTerm)

if len(linkList) > 0:
    for i in linkList:
        print(i + "\n")
    dl = input("Would you like to download? ")
    if dl.upper() in yesList:
        x = 0
        for f in linkList:
            if os.path.isdir(home + '/Documents/Articles'):
                try:
                    pdfkit.from_url(f, home + '/Documents/Articles/' + nameList[x] + '.pdf', configuration=config)
                except:
                    print("Unable to convert website.")
            else:
                try:
                    os.mkdir(home + '/Documents/Articles')
                    pdfkit.from_url(f, home + '/Documents/Articles/' + nameList[x] + '.pdf', configuration=config)
                except:
                    print("Unable to create file directory")
                    
            x += 1
else:
    print("No items found")

