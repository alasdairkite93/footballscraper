import sys
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import pandas as pd
import xlwt
from xlwt import Workbook
import openpyxl
import xlsxwriter
import os
from Naked.toolshed.shell import execute_js, muterun_js
from datetime import date

import pyqt as p

class Setting:

    def __init__(self, sport):
        self.sport = sport

    def urlBuild(self):

        #the role of the urlBuild is to access the ids of each of the upcoming sporting events for the competition


        try:
            with open('mainpage.json') as f:
                data = json.load(f)
                print(data)
                attachment = data['attachments']
                competitions = attachment['competitions']
                events = attachment['events']


                # segment obtains the eventsids of each URL
                eventsids = []
                for key, value in events.items():
                    eventsids.append((key, value['name']))

                todaysURLs = []


                for id in eventsids:

                    if self.sport == 'football':

                        startofURL = 'https://apisds.paddypower.com/sdspp/event-page/v5?_ak=vsd0Rm5ph2sS2uaK&betexRegion=GBR&capiJurisdiction=intl&countryCode=GB&currencyCode=GBP&eventId='
                        eventid = id[0]  # this is a variable that will change
                        endofURL = '&exchangeLocale=en_GB&includeBettingOpportunities=true&includePrices=true&includeSeoCards=true&includeSeoFooter=true&language=en&loggedIn=false&priceHistory=1&regionCode=UK'
                        URL = startofURL + eventid + endofURL
                        todaysURLs.append(URL)


                        startofshots = 'https://apisds.paddypower.com/sdspp/event-page/v5?_ak=vsd0Rm5ph2sS2uaK&betexRegion=GBR&capiJurisdiction=intl&countryCode=GB&currencyCode=GBP&eventId='
                        eventid = id[0]
                        endofshots = '&exchangeLocale=en_GB&includeBettingOpportunities=true&includePrices=true&includeSeoCards=true&includeSeoFooter=true&language=en&loggedIn=false&priceHistory=1&regionCode=UK&tab=shots'
                        shotsurls = startofshots+eventid+endofshots
                        todaysURLs.append(shotsurls)

                        betbuilder = 'https://apisds.paddypower.com/sdspp/event-page/v5?_ak=vsd0Rm5ph2sS2uaK&betexRegion=GBR&capiJurisdiction=intl&countryCode=GB&currencyCode=GBP&eventId='
                        eventid = id[0]
                        endbetbuilder = '&exchangeLocale=en_GB&includeBettingOpportunities=true&includePrices=true&includeSeoCards=true&includeSeoFooter=true&language=en&loggedIn=false&priceHistory=1&regionCode=UK&tab=bet-builder'
                        betsurl = betbuilder+eventid+endbetbuilder
                        todaysURLs.append(betsurl)

                    elif self.sport == 'basketball':

                        betbuilder = 'https://apisds.paddypower.com/sdspp/event-page/v5?_ak=vsd0Rm5ph2sS2uaK&betexRegion=GBR&capiJurisdiction=intl&countryCode=GB&currencyCode=GBP&eventId='
                        eventid = id[0]
                        endbetbuilder = '&exchangeLocale=en_GB&includeBettingOpportunities=true&includePrices=true&includeSeoCards=true&includeSeoFooter=true&language=en&loggedIn=false&priceHistory=1&regionCode=UK&tab=all-markets'
                        betsurl = betbuilder + eventid + endbetbuilder
                        todaysURLs.append(betsurl)


                # todaysURLs.append("https://apisds.paddypower.com/sdspp/content-managed-page/v7?_ak=vsd0Rm5ph2sS2uaK&betexRegion=GBR&capiJurisdiction=intl&cardsToFetch=20351&countryCode=GB&currencyCode=GBP&eventTypeId=1&exchangeLocale=en_GB&includeEuromillionsWithoutLogin=false&includeMarketBlurbs=true&includePrices=true&includeRaceCards=true&language=en&layoutFetchedCardsOnly=true&loggedIn=false&nextRacesMarketsLimit=3&page=SPORT&priceHistory=3&regionCode=UK&requestCountryCode=GB&staticCardsIncluded=SEO_CONTENT_SUMMARY&timezone=Europe%2FLondon")
                file = open('urls.txt', "w")
                for URL in todaysURLs:
                    file.write(URL)
                    file.write('\n')
                file.close()

        except FileNotFoundError as e:
            pass
        except UnicodeDecodeError:
            pass

    #function to clear current files from directory
    def setUp(self):

        directory = 'fixtures'
        try:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
        except FileNotFoundError:
            pass

        try:
            excelpath = 'output.xlsx'
            os.remove(excelpath)
        except FileNotFoundError:
            pass

    def nbascrape(self):

        refs = []
        one_made_threes = "1+_MADE_THREES"
        two_made_threes = "2+_MADE_THREES"
        three_made_threes = "3+_MADE_THREES"
        five_made_threes = "5+_MADE_THREES"
        four_rebounds = "TO_RECORD_4+_REBOUNDS"
        six_rebounds = "TO_RECORD_6+_REBOUNDS"
        eight_rebounds = "TO_RECORD_8+_REBOUNDS"
        ten_rebounds = "TO_RECORD_10+_REBOUNDS"
        twelve_rebounds = "TO_RECORD_12+_REBOUNDS"
        fourteen_rebounds = "TO_RECORD_14+_REBOUNDS"
        sixteen_rebounds = "TO_RECORD_16+_REBOUNDS"
        ten_points = "TO_SCORE_10+_POINTS"
        fifteen_points = "TO_SCORE_15+_POINTS"
        twenty_points = "TO_SCORE_20+_POINTS"
        twenty_five_points = "TO_SCORE_25+_POINTS"
        thirty_points = "TO_SCORE_30+_POINTS"
        thirty_five_points = "TO_SCORE_35+_POINTS"

        refs.append(one_made_threes)
        refs.append(two_made_threes)
        refs.append(three_made_threes)
        refs.append(five_made_threes)
        refs.append(four_rebounds)
        refs.append(six_rebounds)
        refs.append(eight_rebounds)
        refs.append(ten_rebounds)
        refs.append(twelve_rebounds)
        refs.append(fourteen_rebounds)
        refs.append(sixteen_rebounds)
        refs.append(ten_points)
        refs.append(fifteen_points)
        refs.append(twenty_points)
        refs.append(twenty_five_points)
        refs.append(thirty_points)
        refs.append(thirty_five_points)

        data = self.accessdict(refs)
        return data


    def scraper(self):

        refs = []
        ref_one_shot = "PLAYER_TO_HAVE_1_OR_MORE_SHOTS"
        ref_two_shot = "PLAYER_TO_HAVE_2_OR_MORE_SHOTS"
        ref_three_shot = "PLAYER_TO_HAVE_3_OR_MORE_SHOTS"
        ref_four_shot = "PLAYER_TO_HAVE_4_OR_MORE_SHOTS"
        ref_one_foul = "PLAYER_TO_COMMIT_1_OR_MORE_FOULS"
        ref_two_foul = "PLAYER_TO_COMMIT_2_OR_MORE_FOULS"
        ref_pass_30 = "PLAYER_TO_ATTEMPT_30_OR_MORE_PASSES"
        ref_pass_50 = "PLAYER_TO_ATTEMPT_50_OR_MORE_PASSES"
        ref_pass_70 = "PLAYER_TO_ATTEMPT_70_OR_MORE_PASSES"
        ref_pass_90 = "PLAYER_TO_ATTEMPT_90_OR_MORE_PASSES"
        ref_one_shot_target = "PLAYER_TO_HAVE_1_OR_MORE_SHOTS_ON_TARGET"
        ref_two_shot_target = "PLAYER_TO_HAVE_2_OR_MORE_SHOTS_ON_TARGET"
        ref_three_shot_target = "PLAYER_TO_HAVE_3_OR_MORE_SHOTS_ON_TARGET"
        ref_four_shot_target = "PLAYER_TO_HAVE_4_OR_MORE_SHOTS_ON_TARGET"


        refs.append(ref_two_shot)
        refs.append(ref_one_foul)
        refs.append(ref_two_foul)
        refs.append(ref_pass_30)
        refs.append(ref_pass_50)
        refs.append(ref_pass_70)
        refs.append(ref_pass_90)
        refs.append(ref_one_shot_target)
        refs.append(ref_two_shot_target)
        refs.append(ref_three_shot_target)
        refs.append(ref_four_shot_target)
        refs.append(ref_one_shot)
        refs.append(ref_three_shot)
        refs.append(ref_four_shot)

        data = self.accessdict(refs)

        return data

    def accessdict(self, refs):

        print("Access Dict")

        directory = 'fixtures'
        dict = {}

        for r in refs:
            li_example = []
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    with open(file_path) as f:
                        try:

                            data = json.load(f)
                            attachment = data['attachments']
                            markets = attachment['markets']

                            for key, value in markets.items():
                                if markets[key]['marketType'] == r:
                                    try:
                                        for runner in markets[key]['runners']:
                                            odds = runner['winRunnerOdds']
                                            trueodds = odds['trueOdds']
                                            decimalodds = trueodds['decimalOdds']
                                            f_odds = round(decimalodds['decimalOdds'], 2)
                                            li_example.append([runner['runnerName'], f_odds])
                                        print(li_example)
                                    except KeyError as e:
                                        print(e)
                                        pass
                        except KeyError as e:
                            pass
                        except UnicodeDecodeError:
                            pass
            dict[r] = li_example
        return dict


    def generateJson(self):


        response = muterun_js('betfair.js')
        if response.exitcode == 0:
            print(response.stdout)
        else:
            execute_js('betfair.js')

    def getJson(self):

        if self.sport == 'football':
            response = muterun_js('getjson.js')
            if response.exitcode == 0:
                print("exit code 0")
                print('\n')
            else:
                execute_js('getjson.js')

        elif self.sport == 'basketball':
            response = muterun_js('getjsonbball.js')
            if response.exitcode == 0:
                print("exit code 0")
                print('\n')
            else:
                execute_js('getjson.js')

    def writeToExcel(self, li):


        dfs = []
        print("write to excel li ", li)

        for key, value in li.items():
            try:
                print("key: ", key, "value: ", value)
                val1, val2 = map(list, zip(*value))
                df = pd.DataFrame({key : val1, 'odds' : val2})
                dfs.append(df)
            except ValueError:
                pass

        startcol =0
        with pd.ExcelWriter('output.xlsx') as writer:
            for df in dfs:
                try:
                    print(df)
                    df.to_excel(writer, engine="xlsxwriter", startcol=startcol)
                    startcol += 3
                except:
                    pass



#competitions key is for the wider events being played

#The competition id will tell you what the Cup game that the game is being played in
#Selection id will give you the players name
#Event id will tell you the fixture that they are playing
#Event type describes the kind of sport being played

