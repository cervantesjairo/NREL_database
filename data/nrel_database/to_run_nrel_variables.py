from data.nrel_database.nrel_variables import NrelVar
from datetime import datetime


var = 'ghi,dhi,dni,wind_speed,air_temperature,solar_zenith_angle'
lat = 5.61550507
lon = -73.813285
period_range_from = datetime(2020, 1, 1)
period_range_to = datetime(2020, 12, 31)


nrel_var = NrelVar(var=var, lon=lon, lat=lat, period_range_from=period_range_from, period_range_to=period_range_to)
df = nrel_var.data_variables()
print(df)
