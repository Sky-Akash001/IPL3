from django.shortcuts import render
import joblib
import sys
import time
from bs4 import BeautifulSoup
import requests
import pandas


def news(request):

    try:
        page=requests.get('https://www.cricbuzz.com/')

    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()
        print('ERROR FOR LINK:',url)
        print(error_type,'Line:',error_info.tb_lineno)
    time.sleep(2)
    soup=BeautifulSoup(page.text,'html.parser')
    links=soup.find_all('div',attrs={'class':'cb-nws-intr'})
    news = []
    for x in links:
        news.append(x.text)

    return render(request,'predictions/news.html',{'news':news})

# Create your views here.
def index(request):
    return render(request,'predictions/index.html')

def home(request):
    return render(request,'predictions/home.html')
def test(request):
    return render(request,'predictions/test.html')

def result(request):
    cls = joblib.load('finalize_model.sav')

    lis = []

    T1 = request.GET['Team1']
    # if T1 == 'Mumbai Indians':
    d1 = {'Sunrisers Hyderabad':13,'Mumbai Indians':8,'Delhi Capitals':2,'Chennai Super Kings':0,'Kolkata Knight Riders':7,'Royal Challengers Bangalore':12,'Kings XI Punjab':5,'Rajasthan Royals':10,}

    d2 = {'Mumbai':1,'Rajkot':2,'Indore':3,'Bangalore':4,'Kolkata':5,'Delhi':6,'Mohali':7,'Kanpur':8,'Pune':9,'Jaipur':10,'Chennai':11,'Cape Town':12,'Port Elizabeth':13,'Durban':14,'Centurian':15,'Eastern Cape':16,'Johannesburg':17,'Northern Cape':18,'Bloemfont':19,'Ahmedabad':20,'Cuttack':21,'Jamtha':22,'Dharamshala':23,'Visakhapatnam':24,'Raipur':25,'Ranchi':26,'Abu Dhabi':27,'Sharjah':28,'Dubai':29,'Hyderabad':0}

    d3={'Sunrisers Hyderabad':'img/srh.png','Mumbai Indians':'img/mi.jpg','Delhi Capitals':'img/dc.png','Chennai Super Kings':'img/csk.png','Kolkata Knight Riders':'img/kkr.jpg','Royal Challengers Bangalore':'rcb.png','Kings XI Punjab':'img/kxip.png','Rajasthan Royals':'img/rr.png',}
    Team1=request.GET['Team1']
    for x in d1.items():
        if x[0] == Team1:
            lis.append(x[1])


    Team2=request.GET['Team2']
    for x in d1.items():
        if x[0] == Team2:
            lis.append(x[1])


    # if Team1 == Team2:
    #     raise Exception("Both Teams can't be same!!")

    Toss_Winner = request.GET['Toss_Winner']
    if Toss_Winner == 'Team1':
        lis.append(0.0)
        Toss_Winner=Team1

    else:
        lis.append(1.0)
        Toss_Winner=Team2


    Team_batting_First = request.GET['Team_batting_First']
    if Team_batting_First == 'Team1':
        lis.append(0)
        # lis2.append(Team1)
        Team_batting_First=Team1
    else:
        lis.append(1)
        # lis2.append(Team2)
        Team_batting_First=Team2

    Venue = request.GET['Venue']
    for x in d2.items():
        if x[0] == Venue:
            lis.append(x[1])
            # lis2[Venue] = Venue

    # lis.append(request.GET['Team1'])
    # lis.append(request.GET['Team2'])
    # lis.append(request.GET['Team_batting_First'])
    # lis.append(request.GET['Toss_Winner'])
    # lis.append(request.GET['Venue'])


    print(lis)

    ans = cls.predict([lis])
    if ans == 0.:
        winner = Team1
    else:
        winner = Team2
    #
    for x in d3.items():
        if x[0] == winner:
            link=str(x[1])

    lis2={'Team1':Team1,'Team2':Team2,'Toss_Winner':Toss_Winner,'Team_batting_First':Team_batting_First,'Venue':Venue,'link':link}
    return render(request,'predictions/results.html',{'winner':winner,'lis2':lis2})
