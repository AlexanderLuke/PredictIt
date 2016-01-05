from lxml import html
from email.mime.text import MIMEText
import requests
import time
import datetime
import csv
import smtplib

def fetch(URL,path):
	# Get the relevant data from a URL and xPath
	page = requests.get(URL, verify=False)
  	tree = html.fromstring(page.text)
  	approval = tree.xpath(path)
  	approval = approval.pop()
  	print approval
  	print int(approval)
  	print float(approval)
  	approval = str(float(approval.pop()))

  	if len(str(approval)) < 4:
  		approval = str(approval) + '0'
  	return approval

def csvAdd(add): 
	CsvRow = str(add)
	CsvRow = CsvRow.replace("'","")
	CsvRow = '\n' + CsvRow[1:len(CsvRow)-1]
	print CsvRow
	fd = open('15_12_20_history.csv','a')
	fd.write(CsvRow)
	fd.close()
	return

def emailNotification(market, RCP_url, Predicit_URL, old_value, new_value):
	me = 'luke.j.alexander1@gmail.com'
	username = 'luke.j.alexander1'
	password = 'vernonhills'
	time = str(datetime.datetime.now())
	time = time[5:19]
	subject = 'RCP change at %s' %( time )

	msg = "\r\n".join([
	"From: %s" %me,
	"To: %s" %you,
	"Subject: %s" %subject,
	"",
	"The %s market changed from %f to %f at %s.\n" %(market, old_value, new_value, time),
	"The PredictIt market is at %s and the RCP market is at %s.\n" %(Predicit_URL, RCP_url),
	"Bless Up.\n"
	])

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(me, you, msg)
	server.quit()

print 'penis'

Obama_RCP_url = 'http://www.realclearpolitics.com/epolls/other/president_obama_job_approval-1044.html'
Obama_RCP_path = '//*[@id="polling-data-rcp"]/table/tr[2]/td[4]'
Obama_Pred_url = 'https://www.predictit.org/Market/1771/What-will-Obama''s-average-job-approval-be-at-end-of-day-December-25'
old_Obama_value = fetch(Obama_RCP_url, Obama_RCP_path)
csvAdd(old_Obama_value)

print 'penis'

while True:
	new_Obama_value = fetch(Obama_RCP_url, Obama_RCP_path)
	print 'penis'
	if new_Obama_value != old_Obama_value:
		emailNotification('Obama Approval',Obama_RCP_url,Obama_Pred_url,old_Obama_value,new_Obama_value)
		old_Obama_value = new_Obama_value
		
		currentTime = str(datetime.datetime.now())
		currentTime = currentTime[:19]
		add = currentTime, old_Obama_value
		csvAdd(add)

	time.sleep(5)

