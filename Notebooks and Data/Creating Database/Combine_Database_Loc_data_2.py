def combine_data(comb_data_df_name,climate_var_name,database_name):
    from datetime import datetime
    import os
    import pandas as pd

    comb_data_df = pd.read_csv(comb_data_df_name + '.csv', encoding = 'unicode_escape')
    climate_var_name = climate_var_name
    database_name = database_name
    
    # Read in database
    drought_db = pd.read_csv(database_name + '.csv', encoding = 'unicode_escape')

    # Combining database and data tables according to Year,Month and Location. 
    clim_var = []
    row = 1

    for row in drought_db.itertuples():
        time = row.Year_Month
        loca = row.Location
        clim_var.append(float(comb_data_df.loc[(comb_data_df['Year_Month']== time) & (comb_data_df['Location']== loca)][climate_var_name].values))

    drought_db[climate_var_name] = clim_var    

    drought_db.to_csv('Database_Test_'+ climate_var_name + str(datetime.now().strftime('%Y_%m_%d_%H_%M')) +'.csv')        