from data.api.api_nrel import NrelPhysicalSolarModel as NrelPSM
import pandas as pd
from datetime import datetime, timedelta

class NrelVar(NrelPSM):
    # """
    # This Class Object is a child class of NrelPSM that has the API information to pull NREL data. The class has
    # a special method named __init__ and function definition.
    # - The especial method includes var, lat, lon, period_range_from, period_range_to
    # - The definition pulls data from database and cleans it to return a dataframe
    # :param var: Variables, e.g., 'ghi,dhi,dni,clearsky_ghi,wind_direction,wind_speed,air_temperature,total_precipitable_water,solar_zenith_angle,surface_albedo'
    # :param lat: Latitud, e.g., 4.6095
    # :param lon: Longitud, e.g., -74.0685
    # :param period_range_from: datetime(2020, 1, 1)
    # :param period_range_to: datetime(2020, 12, 31)
    #
    # :returns df: dataframe with the set of solar and meteorological data fields from NREL
    # """
    """
    This code defines a class named "NrelVar" which is a child class of the "NrelPhysicalSolarModel" class, and it includes a method named "init" and a function named "data_variables".

    The "init" method takes in five parameters:

    var: a string of variables separated by commas that represents the variables of interest from the NREL data base. If not provided, the default variables will be used.
    lon: a float that represents the longitude of the location of interest.
    lat: a float that represents the latitude of the location of interest.
    period_range_from: a datetime object that represents the start date of the period of interest.
    period_range_to: a datetime object that represents the end date of the period of interest.
    The "data_variables" function returns a pandas dataframe with the set of solar and meteorological data fields from the NREL database. It pulls data from the NREL database for the given latitude and longitude and period of interest. The data is downloaded in chunks of years and then concatenated. The resulting dataframe is cleaned by renaming columns and dropping unnecessary columns.

    The NrelVar class is intended to be used as a way to access NREL data for a specific location and time period, and it provides flexibility in choosing the variables of interest.
    """
    def __init__(self, var, lon, lat, period_range_from, period_range_to):
        super().__init__()
        self.lon = lon
        self.lat = lat
        self.period_range_from = period_range_from
        self.period_range_to = period_range_to
        self.var = self.variables if not var else var         ### Variables are the default variables of the data base


    def data_variables(self):
        time_series = pd.DataFrame()
        time_series['datetime'] = pd.date_range(start=self.period_range_from, end=self.period_range_to)
        years = pd.unique(pd.DatetimeIndex(time_series['datetime']).year)                                   ### years foe which data will be pulled

        for year in years:
            url = 'https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(
                year=year, lat=self.lat, lon=self.lon, leap=self.leap_year, interval=self.interval_data_base, utc=self.utc,
                name=self.your_name, email=self.your_email, mailing_list=self.mailing_list, affiliation=self.your_affiliation,
                reason=self.reason_for_use, api=self.api_key, attr=self.var)

            pp = 60*8760  # 525600
            if year == 2000 or year == 2004 or year == 2008 or year == 2012 or year == 2016 or year == 2020 or year == 2024:
                pp = 60 * 8784

            if year == years[0]:
                # df0 = pd.read_csv(url) ### only to check units
                df0 = pd.read_csv(url, skiprows=2)
                df0 = df0.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=self.interval_data_base + 'Min', periods=pp / int(self.interval_data_base)))
                info = pd.read_csv(url, nrows=1)
                timezone, elevation = info['Local Time Zone'], info['Elevation']
            else:
                df1 = pd.read_csv(url, skiprows=2)
                df1 = df1.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=self.interval_data_base + 'Min', periods=pp / int(self.interval_data_base)))
                df0 = pd.concat([df0, df1])
                del df1


        '''
        DataFrame Cleaning  #TODO need to scale wind speed at height 
        '''
        start_date = datetime.strptime(self.period_range_to, '%Y-%m-%d')
        end_date = start_date.replace(hour=23)
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')

        df = df0.loc[self.period_range_from: end_date_str] #TODO: fix teh hour range

        new_column_name = {'datetime': 'datetime',
                           'GHI': 'ghi',
                           'DHI': 'dhi',
                           'DNI': 'dni',
                           'Clearsky GHI': 'clearsky_ghi',
                           'Wind Speed': 'wind_speed',
                           'Wind Direction': 'wind_direction',
                           'Temperature': 'air_temperature',
                           'Precipitable Water': 'total_precipitable_water',
                           'Surface Albedo': 'surface_albedo',
                           'Solar Zenith Angle': 'solar_zenith_angle'}

        df = df.rename(columns=new_column_name)
        df = df.drop(columns=['Year', 'Month', 'Day', 'Hour', 'Minute'])
        df = df.reset_index().rename(columns={'index': 'datetime'})

        return df