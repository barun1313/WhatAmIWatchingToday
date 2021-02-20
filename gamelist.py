import requests
import bs4
from datetime import datetime, timedelta

res = requests.get(
    "https://liquipedia.net/ageofempires/Liquipedia:Upcoming_and_ongoing_matches")

soup = bs4.BeautifulSoup(res.text, 'lxml')
matchTables = soup.findAll(
    "table", {"class": "wikitable wikitable-striped infobox_matches_content"})

for matchTable in matchTables:
    if(matchTable.find('td', {"class": "team-left"})):
        # finds the name of the tournament
        tournamentName = matchTable.find('td', {"class": "match-filler bgc-lighter"}).find(
            'div', {"class": "matchticker-tournament-wrapper"}).find('div', {"class": "matchticker-tournament-name"}).find('a').contents[0]

        # caluclates time of the match (converts string to datetime) and then converts it into IST by adding 5.5 hours
        matchTime = matchTable.find('td', {"class": "match-filler bgc-lighter"}).find(
            'span', {"class": "timer-object timer-object-countdown-only"}).contents[0]
        countdownUtc = datetime.strptime(
            matchTime, '%B %d, %Y - %H:%M ')
        countdownIst = countdownUtc + timedelta(hours=5.5)

        # finds the players involved
        leftTeam = matchTable.find('td', {"class": "team-left"})
        rightTeam = matchTable.find('td', {"class": "team-right"})

        if(leftTeam.find('span', {"style": "white-space:pre"})):
            leftName = leftTeam.find(
                'span', {"style": "white-space:pre"}).find('a')

            if leftName is None:
                continue
            leftPlayer = leftName.contents[0]
            rightName = rightTeam.find(
                'span', {"style": "white-space:pre"}).find('a')

            if rightName is None:
                continue
            rightPlayer = rightName.contents[0]
            # countdown = matchTable.find('td', {"class": "match-filler bgc-lighter"}).find(
            #     'span', {"class": "timer-object timer-object-countdown-only"}).contents[0]
            print(leftPlayer, "vs", rightPlayer,
                  ", Tournament Name :", tournamentName, "at", countdownIst)

        elif(leftTeam.find('span', {"class": "team-template-text"})):

            tournamentName = matchTable.find('td', {"class": "match-filler bgc-lighter"}).find(
                'div', {"class": "matchticker-tournament-wrapper"}).find('div', {"class": "matchticker-tournament-name"}).find('a').contents[0]

            matchTime = matchTable.find('td', {"class": "match-filler bgc-lighter"}).find(
                'span', {"class": "timer-object timer-object-countdown-only"}).contents[0]
            countdownUtc = datetime.strptime(
                matchTime, '%B %d, %Y - %H:%M ')
            countdownIst = countdownUtc + timedelta(hours=5.5)

            leftName = leftTeam.find(
                'span', {"class": "team-template-text"}).find('a')
            if leftName is None:
                continue
            leftPlayer = leftName.contents[0]
            rightName = rightTeam.find(
                'span', {"class": "team-template-text"}).find('a')
            if rightName is None:
                continue
            rightPlayer = rightName.contents[0]

            print(leftPlayer, "vs", rightPlayer,
                  ", Tournament Name :", tournamentName, "at", countdownIst)
    else:
        continue
