# Coronavirus data in Washington

# The Data

Two datasets were combined for this project. The first data set is from the Washington Department of Health, and gives
the proportion of cases by industry sector. The second data set is from the covid tracking project, and gives raw 
cummulative case counts from April of 2020 to the present. The combined data set uses the number of cases from the covid tracking project
and the proportion in each industry to get the case counts per 10,000 people per industry. 
Two dataframes are used for visualization and analysis. 

The first dataframe is df, which is from the covid tracking project. 

The columns of this data set are ['Date', 'Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White',
       'Cases_Other', 'Cases_NHPI', 'Cases_Multiracial', 'Cases_LatinX',
       'Cases_Ethnicity_NonHispanic', 'Cases_Ethnicity_Hispanic',
       'Cases_Ethnicity_Unknown', 'Cases_Total', 'Deaths_AIAN', 'Deaths_Asian',
       'Deaths_Black', ... 'Deaths_Total', 'Hospitalizations_AIAN',
       'Hospitalizations_Asian', 'Hospitalizations_Black', ...'Hospitalizations_Hispanic']

The second dataframe is sector_10k, which is the combined dataframe from the two sources. 

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/table2.png" > 

The columns of this data set are ['Cases_Hispanic', 'Cases_White', 'Cases_Asian', 'Cases_Black',
       'Cases_AIAN', 'Cases_Total']
The indexes are ['Health Care', 'Manufacturing', 'Retail', 'Agriculture', 'Food Service',
       'Construction', 'Transportation', 'Public Admin']

The following three graphs show the trend of cases, deaths, and hospitalizations from April 2020 to the present. 
There is a rise in all three categories in this time period, with a big spike around November of 2020. 

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/fig1.png" width="600" height="450" > 

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/fig2.png" width="600" height="450" >

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/fig3.png" width="600" height="450" >

The above graphs show a raw count of cases. However, this is not an accurate representation of which races were most affected, as there are more White people than any other race. Note that even though there are much more White people than Hispanic people, there are still more Hispanic cases. The following graphs are adjusted per 10,000. For number of cases, hospitalizations, and deaths, Hispanics are harder hit than any other race by a huge margin. Black people fare slightly worse than Whites, Asians, and Native Americans, but no where near Hispanics. Why is this the case? It may be that more Hispanics are in industries where you are more likely to contract coronavirus. 

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/fig4.png" width="600" height="450" > 

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/fig5.png" width="600" height="450" > 

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/fig6.png" width="600" height="450" > 


# Analysis 

Is there a significant difference in cases between each industry? The 8 industries are health care, manufacturing, retail, agriculture, food service, construction, transportation and public admininistration. With p < .05, 64 null hypothesis significance tests were carried out. 
As an example, is there a difference in cases between the retail and manufacturing industry? In the dataframe, there are about 202 cases per 10,000 in the manufacturing industry, and about 188 cases per 10,000 in the retail industry. 

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/fig7.png" width="600" height="450" > 


Null hypothesis - There is no difference in corona cases in the retail industry vs the manufacturing industry
Alternative hypothesis - There are more cases in the manufacturing industry than the retail industry
This figure is the distribution of (Cases in retail) - (Cases in manufacturing). Probability of seeing this observed difference or higher given the null hypothesis is 0.285. With a p-value of 0.285, we cannot reject the null hypothesis. 
The following heat map gives the p values between all the industries. 

<img src = "https://github.com/asml09/Capstone_1/blob/main/images/fig8.png" width="800" height="800" > 


In this figure, the diagonal is meaningless, because it is each industry versus itself. The results are repeated across the axis (health care, manufacturing is the same as manufacturing, health care) so looking at one half of the diagonal will give all the information you need. There is a significant difference in cases between the health industry and every other industry. There is a difference between manufacturing and agriculture, construction, transportation, and public admin. Looking at the whole chart, there is a difference between a lot of the industries. 

# Conclusion

The rollout of vaccines in Washington is by tier. Tier 1 and 2 included health care workers. This is in line with the results of the analysis, as the health care industry had more cases than any other industry. However, no other Tier gives priority to people in certain industries, even though some industries other than health care were riskier environments for contracting covid. Also, priority is not given to Hispanics, and they contract covid at more than 3x the rate of whites. In tier 3, vaccines are given to those with 2 or more comorbidities. Comorbidities include obesity and smoking. This doesn't seem right, as someone's race is something that absolutely cannot be helped. Someone's industry is mostly something they cannot help. Some would argue that one could change industries if they were worried about contracting covid, but realistically most do not have this option. Whether someone is obese or smokes is something that people have more control over than their race or occupation. If a ranking of who is most at risk to get covid was used for vaccine distribution insteead of tiers, the results would be more fair and there would be less cases overall. A variety of factors could be used to analyze each persons risk, such as race, occupation, and comorbidities. 





