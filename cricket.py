from bs4 import BeautifulSoup
import requests
import os
import lxml
import time
from fake_useragent import UserAgent
import re
import json

'''
    We retrieve the links of the index pages with A, B, C ...
    and then find the players who have participated in an odi
    and store their names and links in a txt file which we 
    parse later.
'''

baseUrl ='http://www.howstat.com/cricket/Statistics/Players/'
url ='http://www.howstat.com/cricket/Statistics/Players/PlayerMenu.asp'




# Creating a fake user agent
us = UserAgent()
header = {'user-agent':us.chrome}

# response is the response object of the url
try:
    response = requests.get(url , headers = header , timeout =3)
except Exception as e:
    print('Can\'t connect to' ,url)
    exit(0)
soup = BeautifulSoup(response.content , 'lxml')

time.sleep(5)

print("Getting the tags info ....")

link = soup.find('a' , attrs ={'class':'abcList'})['href']

baseLink = link[:len(link)-1] #Removing the 'A' to get a neutral url
baseLink = baseUrl + baseLink

print( "Getting the names of all players , will take about 2 minutes ...")
ALLPLAYERSLINKS =[]
count=0
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    new_link = baseLink + letter
    count+=1
    print('Getting result for player: ', count)
    try:
        PlayerPage = requests.get(new_link , headers =header , timeout = 3)
    except Exception as e:
        print('CAn\'t connect to ' , new_link)
        continue
    playerSoup = BeautifulSoup(PlayerPage.content, 'lxml')
    table = playerSoup.find('table', attrs={'class': 'TableLined'})
    rows = table.find_all('tr')
    for row in rows[2:len(rows) - 1]:
        if row.find_all('td')[4].text.strip() == '':
            continue
        else:
            name =row.find('td').a.text.strip()
            link =baseUrl+row.find('td').a['href']
            country = row.find_all('td')[2].text.strip()

            with open('links.txt' , 'a') as file:
                    file.write(name+'$'+country+','+link)
                    file.write('\n')
                    file.close()










