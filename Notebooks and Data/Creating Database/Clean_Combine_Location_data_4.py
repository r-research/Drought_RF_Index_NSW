def clean_comb(climate_var_name,locations):
    import pandas as pd
    from datetime import datetime
    import os
    
    climate_var_name = climate_var_name #What is the climate_var name used in other function
    locations = locations #List of locations

    # Creating an empty dictionary for dataframes:
    di = {} #dictionary
    for name in locations:
        #Read in csv
        csv_loc = pd.read_csv(climate_var_name + '_' + name + '_' + '2000Jan_2022Mar_28July2022.csv', encoding = 'unicode_escape')
        #Rename first col to Date_Time
        csv_loc.rename(columns = {'Unnamed: 0':'Date_Time'},inplace=True)
        # Creating a new column with Year and Month only
        csv_loc['Year_Month'] = pd.to_datetime(csv_loc['Date_Time'],infer_datetime_format=True).dt.to_period('M')
        # Remove date_time col
        csv_loc.drop('Date_Time', axis = 1, inplace = True)
        # Switch col location
        csv_loc2 = csv_loc[['Year_Month', climate_var_name]]
        # Add column with location name
        csv_loc2.insert(0,'Location', name)
        
        di[name] = csv_loc2

    # Combine all dataframes in the dictionary
    combined_loc_data = pd.concat(di.values(),axis = 0)

    # Save to csv
    combined_loc_data.to_csv('All_Location'+ '_' + climate_var_name + '_' + 'test' + str(datetime.now().strftime('%Y_%m_%d_%H_%M')) + '.csv')