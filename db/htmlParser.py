
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser


class parser:
    def __init__(self, url):
        req = requests.get(url)
        s = req.text
        self.soup = BeautifulSoup(s, "html.parser")
        self.url = url
        self.main = []
        self.client = []
        self.score = []
        self.param = []

    def getData(self):
        for title in self.soup.find_all('title') :
            if title.string.find('404') != -1:
                return False

        type_game = ""
        for h1 in self.soup.find_all('h1') :
            for span in h1.find_all('span') :
                type_game = span.text

        index = 0
        game = []
        for tag in self.soup.find_all('table', class_="tabList titTwoRow") :

            for main in tag.find_all('td', class_="texRight") :
                self.main.append(main.a.get('title'))
            for client in tag.find_all('td', class_="texLeft") :
                self.client.append(client.a.get('title'))
            for score in tag.find_all('td') :
                if score.get('hostid') == None :
                    continue
                self.score.append(score.text)
            for param in tag.find_all('span') :
                self.param.append(param.text)


            for index in range(len(self.main)) :
                data = {"main":"", "client":"", "type":"", "rate":"", "win_rate":"", "lost_rate":""}
                # data = self.gameData()

                if len(self.score) != len(self.main):
                    break
                
                data["main"] = self.main[index]
                data["client"] = self.client[index]
                data["type"] = type_game
                if len(self.param[index*3]) == 0 or self.param[index*3] == "-"or self.param[index*3 + 1] == "-"or self.param[index*3 + 2] == "-" :
                    continue
                data["win_rate"] = self.param[index*3 + 0]
                data["rate"] = float(self.param[index*3 + 1])
                data["lost_rate"] = self.param[index*3 + 2]

                data = []
                data.append(self.main[index])
                data.append(self.client[index])
                data.append(type_game)
                data.append(self.param[index*3 + 0])
                data.append(float(self.param[index*3 + 1]))
                data.append( self.param[index*3 + 2])

                game.append(data)

        return game




