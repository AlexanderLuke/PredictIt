from lxml import html
import requests
import time
import datetime
import csv

# Get all of Predictit Prices
# Get all of the RCP values
# Get the time
# Append everything to a .csv file

def fetch(URL,path):
	# Get the relevant data from a URL and xPath
	page = requests.get(URL)
  	tree = html.fromstring(page.text)
  	approval = tree.xpath(path)
  	approval = str(float(approval.pop()))

  	if len(str(approval)) < 4:
  		approval = str(approval) + '0'
  	return approval

def csvAdd(add): 
	CsvRow = str(add)
	CsvRow = CsvRow.replace("'","")
	CsvRow = '\n' + CsvRow[1:len(CsvRow)-1]
	print CsvRow
	fd = open('DebateHistory.csv','a')
	fd.write(CsvRow)
	fd.close()
	return

Path = '//*[@id="pre"]/div[1]/p/b/text()'
TrumpURL = 'https://www.predictit.org/Contract/1405/Will-Donald-Trump-get-the-most-speaking-time-at-the-first-tier-Fox-Business-debate#data'
RubioURL = 'https://www.predictit.org/Contract/1407/Will-Marco-Rubio-get-the-most-speaking-time-at-the-first-tier-Fox-Business-debate#data'
BushURL = 'https://www.predictit.org/Contract/1409/Will-Jeb-Bush-get-the-most-speaking-time-at-the-first-tier-Fox-Business-debate#data'
CarsonURL = 'https://www.predictit.org/Contract/1406/Will-Ben-Carson-get-the-most-speaking-time-at-the-first-tier-Fox-Business-debate#data'
FiorinaURL = 'https://www.predictit.org/Contract/1410/Will-Carly-Fiorina-get-the-most-speaking-time-at-the-first-tier-Fox-Business-debate#data'
CruzURL = 'https://www.predictit.org/Contract/1408/Will-Ted-Cruz-get-the-most-speaking-time-at-the-first-tier-Fox-Business-debate#data'
KasichURL = 'https://www.predictit.org/Contract/1411/Will-John-Kasich-get-the-most-speaking-time-at-the-first-tier-Fox-Business-debate#data'
PaulURL = 'https://www.predictit.org/Contract/1412/Will-Rand-Paul-get-the-most-speaking-time-at-the-first-tier-Fox-Business-debate#data'

while True:

	TrumpSpeak = fetch(TrumpURL, Path)
	RubioSpeak = fetch(RubioURL, Path)
	BushSpeak = fetch(BushURL, Path)
	CarsonSpeak = fetch(CarsonURL, Path)
	FiorinaSpeak = fetch(FiorinaURL, Path)
	CruzSpeak = fetch(CruzURL, Path)
	KasichSpeak = fetch(KasichURL, Path)
	PaulSpeak = fetch(PaulURL, Path)

	currentTime = str(datetime.datetime.now())
	currentTime = currentTime[:19]

	add = currentTime, TrumpSpeak, RubioSpeak, BushSpeak, CarsonSpeak, FiorinaSpeak, CruzSpeak, KasichSpeak, PaulSpeak
	csvAdd(add)

	time.sleep(20)