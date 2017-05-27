import requests
import datetime
from bs4 import BeautifulSoup as bs
from lxml import html

#link to obtain information about realMadrid's next match
url = 'http://www.realmadrid.com/en/football/schedule'
response = requests.get(url)
html = response.content
soup = bs(html,"lxml")

#getting contents from Real madrid website
opp1 = soup.find('div', {'class': 'm_highlighted_next_game_team'}).strong.contents  #home team
opp2 = soup.find('div', {'class': 'm_highlighted_next_game_team m_highlighted_next_game_second_team'}).strong.contents  #away team
time = soup.find('div', {'class': 'm_highlighted_next_game_info_wrapper'}).time.contents    #time in cet(gmt+2:00)
date = soup.find('header', {'class': 'm_highlighted_next_game_header'}).time.contents   #date of match
location = soup.find('p', {'class': 'm_highlighted_next_game_location'}).contents   #location of the match
matchtype = soup.find('header', {'class': 'm_highlighted_next_game_header'}).span.contents  #matchtype(includes champions league,La liga,Copa del rey etc)

#Storing the values
time1 = time[0].strip()
hour=int(time1[:2])
mins = int(time1[3:5])
date1 = date[0].strip()
year=int(date1[:4])
month=date1[5:7]
if '0' in month:
    month=month[-1:]
month=int(month)
day=int(date1[-2:])

#Converting to IST
hour = hour+3
mins = mins+30
if mins>60:
    hour = hour+1
    mins = mins-60
if hour>=24:
    hour = 00
    day = day+1


"""Printing match details"""
print (matchtype[0],"\n",location[0])
print(opp1[0],"(H) vs ",opp2[0],"(A) \n",str(hour).zfill(2),":",str(mins)," on ",str(day),"/",str(month),"/",str(year))

#Countdown
import time
def countdown(t):
    while t:
        min1, secs = divmod(t, 60)
        hours1, mins = divmod(min1,60)
        days, hours = divmod(hours1, 24)
        timeformat = '{:02d} days {:02d}:{:02d}:{:02d}'.format(days,hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
start = datetime.datetime.now()
end = datetime.datetime(year=year, month=month, day=day, hour=hour)
diff = end - start
countdown(int(diff.total_seconds()))
