import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
#from pyowm import OWM
import youtube_dl
#import vlc
import urllib
import urllib3
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime
import warnings
import boto3
import pdfrw
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QEvent
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QPlainTextEdit, QMainWindow)
from eaglevoice_ui import WidgetGallery


warnings.filterwarnings('ignore', message='Unverified HTTPS request')

#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

style = '''
QPushButton {
    background-color: #006325;
    font-size: 20px;
    color: white;

    min-width:  50px;
    max-width:  50px;
    min-height: 50px;
    max-height: 50px;

    border-radius: 25px;        
    border-width: 1px;
    border-color: #ae32a0;
    border-style: solid;
}
QPushButton:hover {
    background-color: #328930;
    color: yellow;
}
QPushButton:pressed {
    background-color: #80c342;
    color: red;
}    

'''

invoicepdf_datadict = {
   'First Name': 'Bostata',
   'Middle Name': 'company.io',
   'Last Name': 'joe@company.io',
   'Address Line 1': 'my address line',
   'Address Line 2':'',
   'Country':'',
   'State':'',
   'City':'',
   'Zip code':''
}

invoicedf_datadict_voice = {
   'First Name': 'First Name',
   'Middle Name': 'Middle Name',
   'Last Name': 'Last Name',
   'Address Line 1': 'Address Line 1',
   'Address Line 2':'Address Line 2',
   'Country':'Country',
   'State':'',
   'City':'',
   'Zip code':''
}



def voiceResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    #r.energy_threshold = 4000
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        gallery.on_submit_btn_click(answer=command)
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()

    return command


def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    annotations = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    voiceResponse(key)
                    annotation.update(
                        # pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                        pdfrw.PdfDict(AP=data_dict[key], V=data_dict[key])
                    )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


def assistant(command):
    "if statements for executing commands"
    global vc

    if vc:
        #bring contect from AWS Lambda
        if 'account' in command and 'balance' in command:
            voiceResponse('tell me the account number')
            voicecontent = myCommand()
            http = urllib3.PoolManager()
            url="https://3yvf19l8z6.execute-api.us-east-1.amazonaws.com/default/getDataDynamoDB"
            response = http.request('GET',url,fields={'CustID': voicecontent})
            status=json.loads(response.data.decode('utf-8'))['statusCode']
            if status==200:
                content=json.loads(response.data.decode('utf-8'))['body']
                print(content)
                voiceResponse('account balance displayed on chat window')
            else:
                voiceResponse('not able to identify the account balance. please cheack account number is correct')


        if command in ('good bye eagle','stop eagle','hey eagle stop','shutdown eagle','hey eagle shutdown','okay eagle shutdown','okay eagle stop'):
            voiceResponse('Bye bye Sir. Have a nice day')
            sys.exit()
        
        #generate pdf
        if ('generate pdf' in command ) or ('sample invoice' in command):
            INVOICE_TEMPLATE_PATH = '/Volumes/GVSP_SAMUSB/EagleVoice/PDF/HackathonPDFEntry Form.pdf'
            INVOICE_OUTPUT_PATH = 'testinvoice.pdf'
            write_fillable_pdf(INVOICE_TEMPLATE_PATH, INVOICE_OUTPUT_PATH, invoicepdf_datadict)


    #open website
        if 'open' in command:
            reg_ex = re.search('open (.+)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                print(domain)
                url = 'https://www.' + domain
                webbrowser.open(url)
                voiceResponse('The website you have requested has been opened for you Sir.')
            else:
                pass

    #open subreddit Reddit
        if 'open reddit' in command:
            reg_ex = re.search('open reddit (.*)', command)
            url = 'https://www.reddit.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            voiceResponse('The Reddit content has been opened for you Sir.')


    #greetings
        if command in ('hello eagle','hey eagle','okay eagle','good morning eagle','good afternoon eagle','good evening eagle'):
            day_time = int(strftime('%H'))
            if day_time < 12:
                voiceResponse('Hello Sir. Good morning. How can I help you')
            elif 12 <= day_time < 18:
                voiceResponse('Hello Sir. Good afternoon. How can I help you')
            else:
                voiceResponse('Hello Sir. Good evening. How can I help you')

        if command in ('hey eagle help me','okay eagle help me','help me'):
            voiceResponse("""
            You can use these commands and I'll help you out:
            1. Open reddit subreddit : Opens the subreddit in default browser.
            2. Open xyz.com : replace xyz with any website name
            3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
            4. Current weather in {cityname} : Tells you the current condition and temperture
            5. Hello
            6. play me a video : Plays song in your VLC media player
            7. change wallpaper : Change desktop wallpaper
            8. news for today : reads top news of today
            9. time : Current system time
            10. top stories from google news (RSS feeds)
            11. tell me about xyz : tells you about xyz
            """)
    #joke
        if 'joke' in command:
            res = requests.get(
                    'https://icanhazdadjoke.com/',
                    headers={"Accept":"application/json"})
            if res.status_code == requests.codes.ok:
                voiceResponse(str(res.json()['joke']))
            else:
                voiceResponse('oops!I ran out of jokes')

    #top stories from google news
        if 'news for today' in command:
            try:
                news_url="https://news.google.com/news/rss"
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"xml")
                news_list=soup_page.findAll("item")
                for news in news_list[:15]:
                    voiceResponse(news.title.text.encode('utf-8'))
            except Exception as e:
                    print(e)

    #time
        if 'time' in command:
            import datetime
            now = datetime.datetime.now()
            voiceResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

'''
    #current weather
        if 'current weather' in command:
            reg_ex = re.search('current weather in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
                obs = owm.weather_at_place(city)
                w = obs.get_weather()
                k = w.get_status()
                x = w.get_temperature(unit='celsius')
                voiceResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

        if 'email' in command:
            voiceResponse('Who is the recipient?')
            recipient = myCommand()
            if 'rajat' in recipient:
                voiceResponse('What should I say to him?')
                content = myCommand()
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('your_email_address', 'your_password')
                mail.sendmail('sender_email', 'receiver_email', content)
                mail.close()
                voiceResponse('Email has been sent successfuly. You can check your inbox.')
            else:
                voiceResponse('I don\'t know what you mean!')
    #launch any application
'''

'''
        if 'launch' in command:
            reg_ex = re.search('launch (.*)', command)
            if reg_ex:
                appname = reg_ex.group(1)
                appname1 = appname+".app"
                subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
            voiceResponse('I have launched the desired application')
'''
if __name__ == '__main__':
    vc=True

    global gallery

    #voiceResponse('Hello, I am Eagle Voice and I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')
    #voiceResponse('Hello, I am Eagle Voice and I am your personal voice assistant, how can I help you')
    voiceResponse('Hello')
    #loop to continue executing multiple commands

    while True:
        app = QApplication(sys.argv)
        app.setStyleSheet(style)
        gallery = WidgetGallery()
        gallery.resize(400, 400)
        gallery.show()
        #gallery.on_submit_btn_click(answer=)
        sys.exit(app.exec_())
        assistant(myCommand())
