from bs4 import BeautifulSoup
import requests
import os
import lxml
import time
from fake_useragent import UserAgent
import re
import json


# Creating a fake user agent
us = UserAgent()
header = {'user-agent':us.chrome}

BASEURL ='http://www.howstat.com/cricket/Statistics/Players/'


# Retreiving the links from links.txt
names=[]
links=[]
country=[]
with open('links.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        pos_link = line.find('http')
        pos_name =line.find('$')
        links.append(line[pos_link:])
        names.append(line[:pos_name])
        country.append(line[pos_name+1:pos_link-1])
    file.close()

PLAYERINFO={}
PLAYERINFO['name'] =[]
counter=0
print('Total players to be considered: ',len(links))
for index,link in enumerate(links):
    counter += 1
    print('Getting Result for player '+ str(counter) + ': percentage done:' + str((counter*100)/len(links)) + " %%" )
    try:
        res = requests.get(link,headers =header, timeout=3)
    except Exception as e:
        print('Can\'t connect to ', link)
        time.sleep(1)
        continue
    soupnew = BeautifulSoup(res.content, 'lxml')
    try:
        newLink =BASEURL+ soupnew.find('a', attrs={'class':'LinkOff'})['href']
    except Exception:
        continue


    try:
        odires = requests.get(newLink , headers =header , timeout=3)
    except Exception as e:
        print('Can\'t connect to ', newLink)
        time.sleep(1)
        continue
    odisoup = BeautifulSoup(odires.content , 'lxml')
    try:
        performancelink = BASEURL+odisoup.find('a' , attrs={'title':'Analysis of performances in each calendar year'})['href']
    except Exception:
        continue
    try:
        finalres = requests.get(performancelink , headers =header , timeout=3)
    except Exception:
        print('Can\'t connect to ', performancelink)
        time.sleep(1)
        continue
    finalsoup = BeautifulSoup(finalres.content , 'lxml')
    try:
        table =finalsoup.find('table', attrs={'class': 'TableLined'})
    except Exception:
        continue

    rows = table.find_all('tr')

    runinfo = {}  # initializing the dictionary

    # Creating a dictionary runinnfo to store the values year:runs as how many runs scored
    # in that year
    try:
        runinfo = {row.find_all('td')[0].text.strip(): (row.find_all('td')[8]).text.strip() for row in
               rows[1:len(rows) - 1]}
    except Exception as e:
        continue

    try:
        overall_score = rows[-1].find_all('td')[8].text.strip()
    except Exception:
        overall_score = 0

    name = names[index]
    nation =country[index]
    scoreNruns = {}  # this dictionary stores all the results for a name
    scoreNruns = {
        'total': overall_score,
    }
    scoreNruns['runs'] = runinfo
    info = {}
    info[name] = {'runinfo': scoreNruns , 'nationality':nation}
    PLAYERINFO['name'].append(info)



# We store the final dictionary as a json file which we parse later

json = json.dumps(PLAYERINFO, indent=4)
with open('data.json', 'w') as f:
    f.write(json)
    f.close