import time 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
def collect_flight_data(day,flight_direction):
    '''
    This function scrape data from BH airport and return it as table.
    Args:
        day(str): Today (TD) or Tomorrow (TM).
        flight_direction (str): arrivals or departures
    Returns:
        pandas dataframe with 8 columns
    '''
    url = f"https://www.bahrainairport.bh/flight-{flight_direction}?date={day}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    time_list = []
    origin_list = []
    airway_list = []
    gate_list = []
    status_list = []
    flight_list = []
    flights = soup.find_all("div", {"class": f"flight-table-list row dv{flight_direction[:-1].title()}List"}) #ArrivalList
    
    for f in flights:
        time_list.append(f.find('div',class_='col col-flight-time').text.strip())
        origin_list.append(f.find('div',class_='col col-flight-origin').text.strip())
        try:
            airway_list.append(f.find('img')['alt'])
        except:
            airway_list.append(pd.NA)
        gate_list.append(f.find('div',class_='col col-gate').text.strip())
        status_list.append(f.find('div',class_='col col-flight-status').text.strip())
        flight_list.append(f.find('div',class_='col col-flight-no').text.strip())
    flights_data = {'origin':origin_list,
                'flight_number':flight_list,
                'airline':airway_list,
                'gate':gate_list,
                'status':status_list,
                'time':time_list}
    df = pd.DataFrame(flights_data)
    if day == 'TD':
        date = datetime.date.today()
    elif day == 'TM':
        date = datetime.date.today() + datetime.timedelta(days=1)
    df['date']= date
    df['direction'] = flight_direction
    return df
collect_flight_data('TM','departures')
def collect_arr_dep():
    tables = []
    directions = ['arrivals','departures']
    days = ['TD','TM']
    for direction in directions:
        for day in days:
            tables.append(collect_flight_data(day, direction))
            time.sleep(10)
        df = pd.concat(tables)
    return df
def save_data(df):
    today= datatime.date.today()
    path = f'all_flights_data{today}.csv'.replace('-','_')
    df.to_csv(path)

df= collect_arr_dep()
save_data(df)

