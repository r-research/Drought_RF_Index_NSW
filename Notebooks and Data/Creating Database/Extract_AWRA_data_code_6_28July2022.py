def extract_var_from_netcdf(file_name, Location_name, lat_location, lon_location, climate_variable_name):
    from netCDF4 import Dataset
    import numpy as np
    import pandas as pd

    file_name = file_name #input('The file name is')
    Location_name = Location_name #input('What is the name of the location?')
    lat_location = lat_location #float(input('What is latitude to 2 dec. places'))
    lon_location = lon_location #float(input('What is longitude to 2 dec. places'))
    climate_variable_name = climate_variable_name #input('The column name for the climate variable is')

    #Here add the extra file_name
    data = Dataset(file_name +'.nc','r')
    # Get the last key - there are usually time, latitude, longitude, time_bounds, and the name of the variable we want. 
    # print(data.variables.keys())
    # How to get the 0,1,,3 4th key is needed. Get the name of the file and save as a variables
    variable_key = list(data.variables.keys())[4] #https://stackoverflow.com/questions/54488095/python-3-dictionary-key-to-a-string-and-value-to-another-string

    # Extract timeseries for Location
    lat = data.variables['latitude'][:]
    lon = data.variables['longitude'][:]
    time = data.variables['time'][:]

    # print(lat.dtype)
    # print(lat_location.types)

    # Squared difference is used to find the least sq difference to get closest possible latitude in the file
    sq_diff_distance_of_lat = (lat - lat_location)**2 #creating another array with same dimension.
    sq_diff_distance_of_lon = (lon - lon_location)**2

    min_index_lat = sq_diff_distance_of_lat.argmin() #using numpy argmin
    min_index_lon = sq_diff_distance_of_lon.argmin()

    # Set 
    Climate_variables = data.variables[variable_key]
    start_day = int(data.variables['time'][0])
    end_day = int(data.variables['time'][-1])

    # Time
    # Startdate:
    startdate_2 = "01/01/1900"
    ds_startdate = pd.to_datetime(startdate_2) + pd.DateOffset(days=start_day)
    ds_endate = pd.to_datetime(startdate_2) + pd.DateOffset(days=end_day)

    # Build dataframe
    data_range_3 = pd.date_range(start = ds_startdate, end = ds_endate, freq='M') 
    df_2 = pd.DataFrame(0, columns = [climate_variable_name], index = data_range_3)

    #Building array
    dt_2 = np.arange(0,data.variables['time'].size)
    # Deleting extra row to match df_2 length
    dt_2 = np.delete(dt_2,-1,0)

    #Adding values to time array
    for time_index in dt_2:
        df_2.iloc[time_index] = Climate_variables[time_index,min_index_lat,min_index_lon]
    
    print('Saving location: ' + Location_name)
    
    df_2.to_csv(climate_variable_name + '_' + Location_name + '_2000Jan_2022Mar_28July2022.csv')
