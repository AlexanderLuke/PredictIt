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
	page = requests.get(URL, verify=False)
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
	fd = open('history.csv','a')
	fd.write(CsvRow)
	fd.close()
	return

Obama455URL = 'https://www.predictit.org/Contract/1398/Will-Obama''s-average-job-approval-be-455-or-higher-at-end-of-day-November-13#data'
Obama455Path = '//*[@id="pre"]/div[1]/p/b/text()'
Obama450URL = 'https://www.predictit.org/Contract/1399/Will-Obama''s-average-job-approval-be-450-454-at-end-of-day-November-13#data'
Obama450Path = '//*[@id="pre"]/div[1]/p/b/text()'
Obama445URL = 'https://www.predictit.org/Contract/1400/Will-Obama''s-average-job-approval-be-445-449-at-end-of-day-November-13#data'
Obama445Path = '//*[@id="pre"]/div[1]/p/b/text()'
Obama440URL = 'https://www.predictit.org/Contract/1401/Will-Obama''s-average-job-approval-be-440-444-at-end-of-day-November-13#data'
Obama440Path = '//*[@id="pre"]/div[1]/p/b/text()'
Obama439URL = 'https://www.predictit.org/Contract/1402/Will-Obama''s-average-job-approval-be-439-or-lower-at-end-of-day-November-13#data'
Obama439Path = '//*[@id="pre"]/div[1]/p/b/text()'

ObamaRcpURL = 'http://www.realclearpolitics.com/epolls/other/president_obama_job_approval-1044.html'
ObamaRcpPath = '//*[@id="polling-data-rcp"]/table/tr[2]/td[4]/text()'

while True:

	Obama455 = fetch(Obama455URL,Obama455Path)
	Obama450 = fetch(Obama450URL,Obama450Path)
	Obama445 = fetch(Obama445URL,Obama445Path)
	Obama440 = fetch(Obama440URL,Obama440Path)
	Obama439 = fetch(Obama439URL,Obama439Path)

	ObamaRcp = fetch(ObamaRcpURL,ObamaRcpPath)

	currentTime = str(datetime.datetime.now())
	currentTime = currentTime[:19]

	add = currentTime, Obama455, Obama450, Obama445, Obama440, Obama439, ObamaRcp
	csvAdd(add)

	time.sleep(20)