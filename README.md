Coronavirus data in Washington

# The Data

Two datasets were combined for this project. The first data set is from the Washington Department of Health, and gives
the proportion of cases by industry sector. The second data set is from the covid tracking project, and gives raw 
cummulative case counts from April of 2020 to the present. The combined data set uses the number of cases from the covid tracking project
and the proportion in each industry to get the case counts per 10,000 people per industry. 
Two dataframes are used for visualization and analysis. 

The first dataframe is df, which is from the covid tracking project. 

{Table 1}

The columns of this data set are ['Date', 'Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White',
       'Cases_Other', 'Cases_NHPI', 'Cases_Multiracial', 'Cases_LatinX',
       'Cases_Ethnicity_NonHispanic', 'Cases_Ethnicity_Hispanic',
       'Cases_Ethnicity_Unknown', 'Cases_Total', 'Deaths_AIAN', 'Deaths_Asian',
       'Deaths_Black', ... 'Deaths_Total', 'Hospitalizations_AIAN',
       'Hospitalizations_Asian', 'Hospitalizations_Black', ...'Hospitalizations_Hispanic']

The second dataframe is sector_10k, which is the combined dataframe from the two sources. 

{Table 2} 

The columns of this data set are ['Cases_Hispanic', 'Cases_White', 'Cases_Asian', 'Cases_Black',
       'Cases_AIAN', 'Cases_Total']

