from lxml import html
import requests
import time
import datetime
import csv

def fetch(URL,path):
	# Get the relevant data from a URL and xPath
	page = requests.get(URL)
  	tree = html.fromstring(page.text)
  	approval = tree.xpath(path)
  	print approval
  	approval = str(float(approval.pop()))

  	if len(str(approval)) < 4:
  		approval = str(approval) + '0'
  	return approval

ObamaRcpURL = 'http://www.realclearpolitics.com/epolls/other/president_obama_job_approval-1044.html'
ObamaRcpPath = '//*[@id="polling-data-rcp"]/table/tr[2]/td[4]/text()'


value = fetch(ObamaRcpURL,ObamaRcpPath)

print type(value)
print value