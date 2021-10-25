import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup
from decouple import config

now = datetime.datetime.now()  # To generate unique subjects for email


def extract_news(url):
    '''
    Extracts news headlines from url given
    '''
    print('Extracting Hacker News Stories...')
    body = '' # Message Body
    body += ('<b>HN Top Stories:<b>\n' + '<br>' + '-' * 50 + '<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title','valign': ''})):
        body += ((str(i + 1) + ' :: ' + tag.text + '\n' +
                  '<br>') if tag.text != 'More' else '')
    return body

content = extract_news('https://news.ycombinator.com/')
content+=('<br>--------<br>')
content+=('<br><br>End of Message')

print('Composing Email')

# Configuring email server setup
SERVER='smtp.gmail.com'
PORT=587
FROM=config('EMAIL')
TO=config('EMAIL')
PASSWORD=config('PASSWORD')

msg = MIMEMultipart()

msg['Subject']='Top New Stories HN [Automated Email]'+' '+str(now.day)+'-'+str(now.month)+'-'+str(now.year)
msg['From']=FROM
msg['To']=TO

msg.attach(MIMEText(content,'html'))

print('Initiating Server...')

server=smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM,PASSWORD)
server.sendmail(FROM,TO,msg.as_string())

print('Email sent...')

server.quit()