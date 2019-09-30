import requests
from bs4 import BeautifulSoup

class arsScrape:

    mlist = list()
    page = requests.get('https://arstechnica.com/')
    soup = BeautifulSoup(page.content, 'lxml')
    ticker = 1
    links = list()
    names = list()

    def getNext(self):
        cont = self.soup.find(class_='load-more', href=True)
        if cont is not None:
            nextPage = 'https://www.arstechnica.com{}/'.format(cont['href'])
            return nextPage
        else:
            afterFirst = self.soup.find(class_='prev-next-links')
            if afterFirst is not None:
                cont = afterFirst.find(class_='left', href=True)
                if cont is not None:
                    nextPage = 'https://www.arstechnica.com{}'.format(cont['href'])
                    return nextPage

    def addToList(self, alist):
        for link in alist:
            if link['href'] not in self.mlist:
                self.mlist.append(link['href'])



    def populateList(self):
        sections = ['listing listing-top with-feature','listing listing-latest','listing listing-rest', 'tease article ']
        for s in sections:
            articles = self.soup.find_all(class_='{}'.format(s))
            if articles is not None:
                for fullList in articles:
                    a = fullList.find_all('a', class_='overlay', href=True)
                    self.addToList(a)

    def runArsScrape(self):
        while len(self.mlist) < 100:
            page = requests.get(self.getNext())
            self.soup = BeautifulSoup(page.content, 'lxml')
            self.populateList()
            #print('Page {}'.format(self.ticker))
            self.ticker += 1
        
    def getLinks(self, searchTerm):
        for item in self.mlist:
            if searchTerm.upper() in item.upper():
                self.links.append(item)
        return self.links

    def getNames(self, searchTerm):
        for item in self.mlist:
            if searchTerm.upper() in item.upper():
                formattedName = ''
            if 'http://' in item:
                formattedName = item.replace('http://', '')
            elif 'https://' in item:
                formattedName = item.replace('https://', '')
            if '/' in formattedName:
                formattedName = formattedName.replace('/', '-')
            self.names.append(formattedName)
        return self.names

    def runScrape(self):
        while len(self.mlist) < 100:
            self.page = requests.get(self.getNext())
            self.soup = BeautifulSoup(self.page.content, 'lxml')
            self.populateList()



