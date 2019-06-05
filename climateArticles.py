import requests
#import wget
import pdfkit
import os
from bs4 import BeautifulSoup
config = pdfkit.configuration(wkhtmltopdf="wkhtmltox/bin/wkhtmltopdf.exe")
originalPage = 'https://news.ycombinator.com/'
page = requests.get(originalPage)
soup = BeautifulSoup(page.content, 'html.parser')

nextSite = ''
home = os.path.expanduser('~')
linkList = list()
nameList = list()

yesList = "YES, Y, ABSOLUTELY"
noList = "NO, N, NEGATIVE"

searchTerm = input("What would you like to search for? ")
print("Searching hackernews...")


#hackerNews
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

print("Searching Arstechnica...")

originalPage = 'https://arstechnica.com'
page = requests.get(originalPage)
soup = BeautifulSoup(page.content, 'html.parser')

end=False
while end == False:
    if os.path.isdir(home+"/Documents/Articles"):
        t = len(os.path.dirname(home + "/Documents/Articles"))
    else:
        t = 0
    for item in soup.find_all('ol'):
        try:
            check = item.li.a['href']
            if searchTerm.upper() in str(item.li.a['href']).upper():
                nameList.append("Article " + str(t))
                t += 1
                linkList.append(check)
        except Exception as e:
            print("+")
    
    try:
        nextSite = item.find('a', class_ = 'load-more')['href']
        page = requests.get(originalPage + nextSite)
        soup = BeautifulSoup(page.content, 'html.parser')
    except Exception as e:
        end = True
    


if len(linkList) > 0:
    for i in linkList:
        print(i + "\n")
    dl = input("Would you like to download? ")
    if dl.upper() in yesList:
        x = 0
        for f in linkList:
            if os.path.isdir(home + '/Documents/Articles'):
                #pdfkit.from_url(f, home + '/Documents/Articles/' + nameList[x] + '.pdf', configuration=config)
                try:
                    pdfkit.from_url(f, home + '/Documents/Articles/' + nameList[x] + '.pdf', options={'javascript-delay': 2000})
                except Exception as e:
                    print("Problem: " + str(e))
            else:
                try:
                    os.mkdir(home + '/Documents/Articles')
                    #pdfkit.from_url(f, home + '/Documents/Articles/' + nameList[x] + '.pdf', configuration=config)
                    pdfkit.from_url(f, home + '/Documents/Articles/' + nameList[x] + '.pdf', options={'javascript-delay': 2000})
                except:
                    print("Unable to create file directory")
            x += 1
else:
    print("No items found")

