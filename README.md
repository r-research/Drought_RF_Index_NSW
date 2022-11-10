# Drought RF Index for NSW

The following repository includes code used to create a drought RF index for NSW, Australia. The drought impact database has been uploaded too. 

1. Extract local climate variables (LCV) and Modes of Variability (MoV) from netcdf files. 
- Input: Database with latitude and longitude data
- Output: A csv with monthly data from 2000 to 2021 for each coordinate provided
Netcdf files from AWRA-L need to be manually downloaded from here: http://www.bom.gov.au/water/landscape/#/sm/Actual/day/-28.4/130.4/3/Point////2022/11/9/ 
(rain_day_Actual_month.nc, qtot_Actual_month.nc, sm_pct_Actual_month_root_zone.nc, e_actual_tot_Actual_month.nc, pet_Actual_month.nc, deep_drainage_Actual_month.nc)

2. Extract LCV and MoV for each event (year-month) and location in the database

3. Clean the database so that it contains both response variables (drought or non drought events) and the predictor variables (LCV and MoV)

4. Train the RF using scikitlearn RandomForestClassifier

5. Generate metrics of performance on out of sample data - confusion matrix and classification report

6. Compare the RF performance to SPI 1,3,6,12,24 month accumulations at different drought classifications thresholds and CDI at different drought classification thresholds.

7. Generate feature importance figures for all the data and the year 2019

8. Generate drought probability from Jan 2000 till Dec 2021 for all locations. 
