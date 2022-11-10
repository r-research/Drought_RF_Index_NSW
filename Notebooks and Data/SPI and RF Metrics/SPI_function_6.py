def get_SPI_n(climate_var_name,locations,month_acc,prev_database_mth_acc):
    # Date: 1 Sept 2022
    # Author: Shalini Rome

    # Assigning variables
    climate_var_name = climate_var_name
    locations = locations
    month_acc = month_acc
    prev_database_mth_acc = prev_database_mth_acc

    # Importing files
    import pandas as pd
    from datetime import datetime
    import os
    import pandas as pd
    from standard_precip.spi import SPI
    from standard_precip.utils import plot_index
    from glob import glob

    # Setting rainfall name variable: Put that as input
    ##climate_var_name = 'Rainfall' #What is the climate_var name used in other function

    # Get locations list:
    df_prac = pd.read_csv('C:/Users/sy6sh/Documents/A.UNSW_COURSE_FOLDERS/Honours 2022/Coding/28 July Coding/Drought_Impact_Database_28July2022_.csv', encoding = 'unicode_escape')
    df_prac.drop_duplicates(subset = ["Location"],inplace = True)
    list_of_locations = df_prac['Location'].tolist()
    # Setting it for the below function.
    locations = list_of_locations #List of locations

    # Creating an empty dictionary for dataframes:
    di = {} #dictionary

    # Loop
    for name in locations:
        #Read in csv
        csv_rain = pd.read_csv('C:/Users/sy6sh/Documents/A.UNSW_COURSE_FOLDERS/Honours 2022/Coding/28 July Coding/' + climate_var_name + '_' + name + '_' + '2000Jan_2022Mar_28July2022.csv', encoding = 'unicode_escape')
        #Rename first col to Date_Time
        csv_rain.rename(columns = {'Unnamed: 0':'Date_Time'},inplace=True)
        # Creating a new column with Year and Month only
        csv_rain['Year_Month'] = pd.to_datetime(csv_rain['Date_Time'],infer_datetime_format=True).dt.to_period('M')
        # Remove date_time col
        csv_rain.drop('Date_Time', axis = 1, inplace = True)
        # Switch col location
        csv_rain2 = csv_rain[['Year_Month', climate_var_name]]

        # Change year_month data type form yyyy-mm to yyyy-mm-dd (The SPI function needs this)
        # Source: https://stackoverflow.com/questions/59316865/typeerror-passing-perioddtype-data-is-invalid-use-data-to-timestamp-instea
        csv_rain2['Year_Month'] = csv_rain2['Year_Month'].dt.to_timestamp('s').dt.strftime('%Y-%m-%d')

        # Calculate SPI here: 
        csv_rain2.rename(columns={"Year_Month":"date","Rainfall":"precip"},inplace = True)
        spi_rain = SPI()
        spi_monthly = spi_rain.calculate(csv_rain2, 'date', 'precip', freq="M", scale=month_acc, 
                                        fit_type="lmom", dist_type="gam")
        
        # Add column with location name
        spi_monthly.insert(0,'Location', name)

        di[name] = spi_monthly
        
    # Combine all dataframes in the dictionary
    combined_SPI_data = pd.concat(di.values(),axis = 0)

    # Save to csv
    combined_SPI_data.to_csv('All_Location'+ '_' + climate_var_name + '_SPI_'+ str(month_acc) +'_' + str(datetime.now().strftime('%Y_%m_%d')) + '.csv')
    print('Calculated SPI for all locations')


    # Extracting SPI monthly and appending to Database. 
    # Now we don't know the very end of the file name. So... we will use the solution suggested here: https://stackoverflow.com/questions/67642228/reading-a-csv-file-without-the-full-name

    # drought_db = pd.read_csv('Database_All_AWRA_NDVI_MOf_and_3MPrecip_noWel_SPI_'+ str(prev_database_mth_acc) +'month_data' + str(datetime.now().strftime('%Y_%m_%d_%H_%M'))+ '.csv', encoding = 'unicode_escape')
    
    file = glob('Database_All_AWRA_NDVI_MOf_and_3MPrecip_noWel_SPI_'+ str(prev_database_mth_acc) +'month_data*.csv')[0] 
    drought_db = pd.read_csv(file, encoding = 'unicode_escape')

    # SPI_6_df = combined SPI data but the date has changed to be yyyy-mm. HOw to convert.
    
    # Data format: date - yyyy-mm-mm, TotalPrecipitation - 0.00
    # My format: Location, Year_Month - yyyy-mm, Rainfall
    # Change year_month data type form yyyy-mm to yyyy-mm-dd (The SPI function needs this)
    # Source: https://stackoverflow.com/questions/59316865/typeerror-passing-perioddtype-data-is-invalid-use-data-to-timestamp-instea
    combined_SPI_data['date'] = combined_SPI_data['date'].dt.strftime('%Y-%m')
    combined_SPI_data.drop(['precip_scale_'+ str(month_acc)],axis = 1,inplace = True)
    combined_SPI_data.rename(columns={"date":"Year_Month"},inplace = True)
    # Combining database and data tables according to Year,Month and Location. 
    clim_var_2 = []
    row = 1

    r_name = 'precip_scale_'+ str(month_acc) +'_calculated_index'
    #For SPI
    for row in drought_db.itertuples():
        time = row.Year_Month
        loca = row.Location
        # print(row)
        clim_var_2.append(float((combined_SPI_data.loc[(combined_SPI_data['Year_Month']== time) & (combined_SPI_data['Location']== loca)][r_name].values)))

    drought_db[r_name] = clim_var_2
    drought_db.to_csv('Database_All_AWRA_NDVI_MOf_and_3MPrecip_noWel_SPI_'+ str(month_acc) +'month_data' + str(datetime.now().strftime('%Y_%m_%d_%H_%M')) +'.csv')
    print('Successfully extracted SPI for '+ str(month_acc)+' months and added to database')