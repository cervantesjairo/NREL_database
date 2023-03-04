# ################################################################################
# # https://developer.nrel.gov/docs/solar/nsrdb/psm3-download/
# # https://developer.nrel.gov/docs/solar/nsrdb/python-examples/
# # https://docs.python.org/3/library/string.html#format-string-syntax

class NrelPhysicalSolarModel:
    '''
    This Class object has the API information associated with Physical Solar Model (PSM) v3 database of the
    National Renewable Energy Laboratory (NREL).
     - A configurable set of solar and meteorological data fields from The NSRDB.
     - Satellite-derived measurements of solar radiation—global horizontal, direct normal,
      and diffuse horizontal irradiance—and meteorological data.
     - These data have been collected at a sufficient number of locations and temporal and spatial scales to accurately
     represent regional solar radiation climates. The data are publicly available at no cost to the user.
      These API provide access to downloading the data.
     - Visit: https://developer.nrel.gov/docs/solar/nsrdb/psm3-download/
    - Visit: https://developer.nrel.gov/docs/solar/nsrdb/python-examples/

    '''
    def __init__(self):
        self.api_key = 'FVltdchrxzBCHiSNF6M7R4ua6BFe4j81fbPp8dDP'
        self.variables = 'ghi,dhi,dni,clearsky_ghi,wind_direction,wind_speed,air_temperature,total_precipitable_water,solar_zenith_angle,surface_albedo'
        self.mailing_list = 'false'
        self.your_name = 'Jairo+Cervantes'
        self.reason_for_use = 'research'
        self.your_affiliation = 'UNL'
        self.your_email = 'jairo.cervantes@huskers.unl.edu'
        self.leap_year = 'true'             # Set leap year to true or false. True will return leap day data if present, false will not.
        self.interval_data_base = '60'      # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
        self.utc = 'false'