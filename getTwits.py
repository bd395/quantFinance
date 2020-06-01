
def getTwits(tix, static_info=False): 

    # Data handling imports

    import yfinance as yf
    import pandas as pd
    import numpy as np
    from datetime import date

    # Webscraping imports

    import json
    import re

    import requests 
    from bs4 import BeautifulSoup
    
    # Attributes

    static_attributes = ['symbol','exchange', 'sector', 'industry', 'type' ]
    daily_attributes = ['date','trending', 'trendingScore', 'sentimentChange', 'volumeChange', 'price', 'change',
                        'percent', 'lastUpdated', 'extendedHoursChange', 'open', 'outcome', 'last', 'extendedHoursPrice',
                        'easternDateTime', 'previousCloseDate', 'previousClose', 'dateTime', 'volume', 'lastSize', 'low',
                        'percentChange', 'high', 'extendedHoursPercentChange', 'extendedHoursDateTime']
    
    # Initializing pandas dataframe for static data

    attr_df = pd.DataFrame(columns=static_attributes, index=tix)

    # Initializing pandas dataframes for daily data

    tix_df_list = []

    for tick in tix:
        globals()['{}_df'.format(tick)] = pd.DataFrame(columns=daily_attributes, index=np.arange(100))
        tix_df_list.append(globals()['{}_df'.format(tick)])


    for j in range(len(tix)):
    #for tick in tix:
        symbol = tix[j]
        url = "https://stocktwits.com/symbol/{}".format(symbol)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        script = soup.find_all("script")
        pattern = re.compile('window.INITIAL_STATE = {.*}')

        for i in script:
            strObj = i.text
            match = pattern.search(strObj)
            if match:
                start_str = strObj.find('window.INITIAL_STATE')
                front_str = strObj[start_str:] # front is proper
                end_str = front_str.find(';') # find end
                good_str = front_str[:end_str]
                jsonString = good_str.split("window.INITIAL_STATE = ")[1][:].encode('utf8').decode('unicode_escape')
                jsonData = json.loads(jsonString, strict=False)


        # LOOP THROUGH STATIC AND DAILY ATTRIBUTES TO BUILD OUT PANDAS DATAFRAMES

        #print(jsonData)
        if static == True:
            for static in static_attributes:
                attr_df.loc["{}".format(symbol), static] = jsonData['stocks']['inventory'] \
                                                                    ['{}'.format(symbol)][static]

        # Change this everyday, 0 = 5/31/2020
        daily_row = 0
        # could load this into a pickle


        z = 1
        for daily in daily_attributes:
            if daily == "date":
                tix_df_list[j].iloc[daily_row, 0] = date.today()
            else:
                tix_df_list[j].iloc[daily_row, z] = jsonData['stocks']['inventory'] \
                                                            ['{}'.format(symbol)][daily]
                z += 1
                
        return tix_df_list, attr_df
