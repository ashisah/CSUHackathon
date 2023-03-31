from lxml import html
from bs4 import BeautifulSoup 
import re
import requests
import csv

# this is how the data is structred
class Kit:
    def __init__(self, id, dateCreated, currentStatus, statuses):
        self.id=id
        self.dateCreated=dateCreated
        self.currentStatus=currentStatus
        self.statuses=statuses
        
# make csv file
with open('kits.csv', mode='w') as csvfile:
    fieldnames = ['id', 'date_created', 'current_status', 'status_history']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for x in range(200000,400000):
        # generate URL
        url = "https://sakt.ohioattorneygeneral.gov/timeline?serialNumber="
        i=6-len(str(x))
        ID=""
        
        for j in range(i):
            ID+='0'
            
        ID+=str(x)
        url+=ID
        # request html
        page = requests.get(url)
        # parse html
        soup = BeautifulSoup(page.text, 'html.parser')
        tree = html.fromstring(page.content)
        # get list of statuses
        results = soup.find_all('div', attrs={'class':'coc-assignment-tile'})
        statuses=[]
        
        for result in results:
            result = result.find('div').text
            result=result.strip()
            result=re.sub('\n', '', result)
            result=" ".join(result.split())
            statuses.append(result)
            
        # get current status
        curStatus = tree.xpath('/html/body/div[1]/div/div[2]/div/div/strong/text()')
        # get date created
        dateCreated = tree.xpath('/html/body/div[1]/div/div[3]/div[1]/div/div/strong/text()')
        # make sure its not a valid kit
        
        if(len(dateCreated)==0):
            continue
            
        curStatus=curStatus[0]
        dateCreated=dateCreated[0][8:]
        # store data
        k = Kit(ID, dateCreated, curStatus, statuses)
        writer.writerow({"id":ID, "date_created":dateCreated, "current_status":curStatus, "status_history":statuses})
