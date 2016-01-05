from lxml import html
import requests
import smtplib
from email.mime.text import MIMEText
import time
import datetime

# Fetch the value for a given market from RCP
def get_RCP_value(URL,path):
  page = requests.get(URL)
  tree = html.fromstring(page.text)
  approval = tree.xpath(path)
  approval = float(approval[0])
  return approval

# Send email to notify of actionable change in market
def send_email(option,URL):
  me = 'luke.j.alexander1@gmail.com'
  you = 'luke.j.alexander1@gmail.com,dxseangt@gmail.com'
  username = 'luke.j.alexander1'
  password = 'vernonhills'
  msg = "\r\n".join([
    "From: %s" %me,
    "To: %s" %you,
    "Subject: %s" %option,
    "",
    "%s" %URL
    ])
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.ehlo()
  server.starttls()
  server.login(username,password)
  server.sendmail(me, you, msg)
  server.quit()
  console = str(datetime.datetime.now())
  console = console[:19]
  print console + ' >> Email sent ---------------------------------------------'

# Determine the appropriate share to buy for a given RCP value
def classify(market,value):
  if market == 'Obama':
    LowBound = 44.9
    Bound1 = 45.0
    Bound2 = 45.4
    Bound3 = 45.5
    Bound4 = 45.9
    Bound5 = 46.0
    Bound6 = 46.4
    HighBound = 46.5
    if value < Bound1:
      option = 'Buy Obama Under 44.9'
    elif value > LowBound and value < Bound3:
      option = 'Buy Obama 45.0 - 45.4'
    elif value > Bound2 and value < Bound5:
      option = 'Buy Obama 45.5 - 45.9'
    elif value > Bound4 and value < HighBound:
      option = 'Buy Obama 46.0 - 46.4'
    elif value > Bound6:
      option = 'Buy Obama Above 46.5'
  elif market == 'Congress':
    Bound1 = 15.2
    Bound2 = 15.1
    if value < Bound1:
      option = 'Sell Congress'
    elif value > Bound2:
      option = 'Buy Congress'
  elif market == 'Direction':
    Bound1 = 28.0
    Bound2 = 27.9
    if value < Bound1:
      option = 'Sell Direction'
    elif value > Bound2:
      option = 'Buy Direction'
  elif market == 'Bush':
    Bound1 = 10.0
    Bound2 = 9.9
    if value < Bound1:
      option = 'Sell Bush'
    elif value > Bound2:
      option = 'Buy Bush'
  return option

# Check to see if the old and new value dictate diffrent shares to buy
def check(value_new,value_old,market):
  if value_new == value_old:
    return 'No action'
  else:
    option_old = classify(market,value_old)
    option_new = classify(market,value_new)
    if option_new == option_old:
      return 'No action'
    else:
      return option_new

# Find initial values
Obama_URL = 'http://www.realclearpolitics.com/epolls/other/president_obama_job_approval-1044.html'
Obama_path = '//*[@id="polling-data-rcp"]/table/tr[2]/td[4]/text()'
Obama_predictit = 'https://www.predictit.org/Market/1580/What-will-Obama''s-average-job-approval-be-at-end-of-day-September-25'

Congress_URL = 'http://www.realclearpolitics.com/epolls/other/congressional_job_approval-903.html'
Congress_path = '//*[@id="polling-data-rcp"]/table/tr[2]/td[4]/text()'
Congress_predictit = 'https://www.predictit.org/Contract/1223/Will-congressional-job-approval-be-at-least-15-on-September-25#data1'

Direction_URL = 'http://www.realclearpolitics.com/epolls/other/direction_of_country-902.html'
Direction_path = '//*[@id="polling-data-rcp"]/table/tr[2]/td[4]/text()'
Direction_predictit = 'https://www.predictit.org/Contract/1222/Will-Right-Direction-poll-at-295-on-September-25#data1'

Bush_URL = 'http://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html'
Bush_path = '//*[@id="polling-data-rcp"]/table/tr[2]/td[6]/text()'
Bush_predictit = 'https://www.predictit.org/Contract/1176/Will-primary-polling-give-Bush-at-least-10-on-September-30#data1'

Obama_approval = get_RCP_value(Obama_URL,Obama_path)
Congress_approval = get_RCP_value(Congress_URL,Congress_path)
Direction_of_country = get_RCP_value(Direction_URL,Direction_path)
Bush_approval = get_RCP_value(Bush_URL,Bush_path)

# Enter loop comparing old and new values to detect changes
while True:

  # Get a new value for each market
  Obama_new = get_RCP_value(Obama_URL,Obama_path)
  Congress_new = get_RCP_value(Congress_URL,Congress_path)
  Direction_new = get_RCP_value(Direction_URL,Direction_path)
  Bush_new = get_RCP_value(Bush_URL,Bush_path)

  # Check if there is a difference in the old and new values, determine correct action
  action1 = check(Obama_new,Obama_approval,'Obama')
  action2 = check(Congress_new,Congress_approval,'Congress')
  action3 = check(Direction_new,Direction_of_country,'Direction')
  action4 = check(Bush_new,Bush_approval,'Bush')

  # If an email needs to be sent, send it
  if action1 != 'No action':
    action1 = 'Obama approval just changed from %d to %d on RCP' %(Obama_approval, Obama_new)
    send_email(action1,Obama_predictit)
    Obama_approval = Obama_new

  if action2 != 'No action':
    action2 = 'Congressional approval just changed from %d to %d on RCP' %(Congress_approval,Congress_new)
    send_email(action2,Congress_predictit)
    Congress_approval = Congress_new

  if action3 != 'No action':
    action3 = 'Direction of country just changed from %d to %d on RCP' %(Congress_approval,Congress_new)
    send_email(action3,Direction_predictit)
    Direction_of_country = Direction_new

  if action4 != 'No action':
    send_email(action4,Bush_predictit)
    Bush_approval = Bush_new

  console = str(datetime.datetime.now())
  console = console[:19]
  print console + ' >> No action'
  
  time.sleep(20)

