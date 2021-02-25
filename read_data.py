# import tabula
# df = tabula.read_pdf("https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables/COVID-19MorbidityMortalityRaceEthnicityLanguageWAState.pdf", 
# pages = 5)
# print(df)

# with open('table1.1.rtf') as f:
#     # lines = f.readlines()
#     # print(lines)
#     for line in f:
#         print(line.strip())
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns; sns.set_theme()

df = pd.read_csv("washington-race.csv", delimiter = ',')

# drop empty columns
# LatinX - ancetry from Latin American countries regardless of language, Hispanic - ancestry from Spanish-speaking countries
    # Combine to Hispanic - includes both these groups in this df
df.drop(['Tests_AIAN', 'Tests_Asian', 'Tests_Black', 'Tests_Ethnicity_Hispanic', 'Tests_Ethnicity_NonHispanic', 'Tests_Ethnicity_Unknown',
    'Tests_LatinX', 'Tests_Multiracial', 'Tests_NHPI', 'Tests_Other', 'Tests_White', 'Tests_Total', 'State'], axis = 1, inplace = True, )
df['Cases_Hispanic'] = df['Cases_Ethnicity_Hispanic'] + df['Cases_LatinX']
df['Deaths_Hispanic'] = df['Deaths_Ethnicity_Hispanic'] + df['Deaths_LatinX']
df['Hospitalizations_Hispanic'] = df['Hospitalizations_Ethnicity_Hispanic'] + df['Hospitalizations_LatinX']
cols = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total',
    'Deaths_Asian', 'Deaths_AIAN', 'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total', 
    'Hospitalizations_Asian', 'Hospitalizations_AIAN', 'Hospitalizations_Black', 'Hospitalizations_White', 
    'Hospitalizations_Hispanic', 'Hospitalizations_Total']
# fill Na with mean of column, change date to DateTime
nan_values = df.isna()
nan_columns = nan_values.any()
columns_with_nan = df.columns[nan_columns].tolist()
for column in columns_with_nan:
    df[column].fillna(value=df[column].mean(), inplace=True)
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')
#df['Hospitalizations_White'].fillna(value=df['Hospitalizations_White'].mean(), inplace=True)
#print(df['Hospitalizations_White'])



def plot_by_date(columns, labels, title, df):
    fig, ax = plt.subplots()
    for tup in zip(columns, labels):
        ax.plot(df['Date'], df[tup[0]], label = tup[1])
    ax.legend()
    ax.set_title(title)
    plt.xticks(rotation = 90)
    ax.tick_params(axis='x', which='major', labelsize=5)
    plt.show()  

Races_cases = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total']
Races_deaths = ['Deaths_Asian', 'Deaths_AIAN', 'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total']
Races_hospitalization = ['Hospitalizations_Asian', 'Hospitalizations_AIAN', 'Hospitalizations_Black', 'Hospitalizations_White', 
    'Hospitalizations_Hispanic', 'Hospitalizations_Total']
Labels = ["Asian", "Native American", "Black", "White", "Hispanic", "Total"]

#plot_by_date(Races_cases, Labels, "Corona cases for all the races", df)
#plot_by_date(Races_deaths, Labels, "Corona deaths for all the races", df)
#plot_by_date(Races_hospitalization, Labels, "Corona hospitalizations for all the races", df)

#print(df.columns)

# df_prop has only the cases. This dataframe sums all the cases from all the days, and they are converted to cases per 10,000 people 
# This is adjusted from the fact that Washington is 9.6% Asian, 1.9% Native American, 4.4% Black, 67.5% White, 13% Hispanic
    # with a population of 7,614,893
# df_prop will only have the first row of df, which is the total number of cases on 02/21/2021 (NOT new cases) as this is the most recent data
num_eachrace = np.array([.096, .019, .044, .675, .13, 1, .096, .019, .044, .675, .13, 1, .096, .019, .044, .675, .13, 1])
num_eachrace *= 7614893
num_eachrace *= (1 / 10000)

num_eachrace = pd.DataFrame([num_eachrace], columns = cols)

# row 3 is cases per 10,000
df_prop = df[cols]
# df_prop = df_prop.loc[0:1, :]
df_prop = df_prop.append(num_eachrace, ignore_index=True)
for i in range(91):
    df_prop.loc[i] = df_prop.loc[i] / df_prop.loc[91]
df_prop['Date'] = df['Date']
df_prop.drop([91], axis = 0, inplace=True)
#print(df_prop)
#plot_by_date(Races_cases, Labels, "Corona cases per 10,000 for all the races", df_prop)
#plot_by_date(Races_deaths, Labels, "Corona deaths per 10,000 for all the races", df_prop)
# plot_by_date(Races_hospitalization, Labels, "Corona hospitalizations per 10,000 for all the races", df_prop)


#df_prop_sector is the first row of df, to be used to merge with the sector data
df_prop_sector = df_prop.loc[0:1, :]
df_prop_sector.drop(['Deaths_Asian', 'Deaths_AIAN',
       'Deaths_Black', 'Deaths_White', 'Deaths_Hispanic', 'Deaths_Total',
       'Hospitalizations_Asian', 'Hospitalizations_AIAN',
       'Hospitalizations_Black', 'Hospitalizations_White',
       'Hospitalizations_Hispanic', 'Hospitalizations_Total', 'Date', 'Cases_Total'], axis = 1, inplace=True)
#df_prop_sector['Sector'] = ['Filler', 'Filler']


df_sector = pd.read_csv("population-percent.csv", delimiter = ',,', engine = 'python')


# print(df_sector.head())
# print(df_prop_sector)

df_sector = df_sector.rename(columns={'Race / Ethnicity': 'Sector', 'Hispanic': 'Cases_Hispanic', 'Non-Hispanic White':'Cases_White', 
    'Non-Hispanic Asian':'Cases_Asian', 'Non-Hispanic Black':'Cases_Black', ' American Indian or Alaska Native': 'Cases_AIAN'})
df_sector.drop(0, axis = 0, inplace = True)

df_sector.drop("Unnamed: 6", axis = 1, inplace = True)
df_sector.reset_index(inplace=True)
df_sector.drop("index", axis = 1, inplace = True)


for cases in Races_cases[0:5]:
    df_sector[cases] = df_sector[cases].str.rstrip('%').astype('float') / 100.0


# print(df_sector.head())
# Now we have all the percents as decimals from rows 0:7, and from 8:9 the number of cummulative cases on 02/21/2021
# Next step: multiply rows -0:7 by row 8, to get cases per 10,000 in each industry sector
sector_final = pd.concat([df_sector, df_prop_sector], ignore_index=True)

#print(sector_final[['Cases_Asian', 'Cases_AIAN']])
Races_cases = ['Cases_Asian', 'Cases_AIAN', 'Cases_Black', 'Cases_White', 'Cases_Hispanic', 'Cases_Total']

temp = sector_final.drop(['Sector'], axis = 1)
for i in range(8):
    temp.loc[i] = temp.loc[i] * temp.loc[8]
#print(temp)
#sector_10k has the cases per industry per 10,000
sector_10k = sector_final[['Sector']].join(temp)
#print(sector_10k[['Sector', 'Cases_Hispanic']])
sector_10k.drop([8, 9], axis = 0, inplace=True)
sector_10k = sector_10k.set_index('Sector')
sector_10k = sector_10k.rename(index = {'"Agriculture, Forestry, Fishing and Hunting"': 'Agriculture',
     'Health Care and Social Assistance' : 'Health Care', 'Accommodation and Food Services': 'Food Service', 
     'Retail Trade': 'Retail', 'Public Administration': 'Public Admin', 'Transportation and Warehousing': 'Transportation'})
#sector_10k.drop(['Sector'], axis = 0, inplace=True)
# print(sector_10k.index)

#Hypothesis testing
# THe health care industry is seen generally as the most dangerous, and thus health care workers were one of the first to 
# receive the vaccine. However, retail and food services also appear to be dangerous trades. Is there a 
# significant difference between the safest job(public administration) and retail, and food services?
# Starting with Hispanics in retail vs Hispanics in public administration 

#Retail - row 2, Public admin - row 7
# print(sector_10k['Cases_Hispanic'])
sector_10k['Cases_Total'] = sector_10k.sum(axis = 1)
print(sector_10k['Cases_Total'])
print(sector_10k.columns)


#Null hypothesis- there is no difference between covid cases in retail and covid cases in public admin
# total_Hisp = sector_10k["Cases_Total"].sum(axis = 0)
# shared_freq = (sector_10k.loc[2, "Cases_Total"] + sector_10k.loc[7, "Cases_Total"]) / total_Hisp
# # print(shared_freq)
# shared_var = (2 * (shared_freq) * (1 - shared_freq))/total_Hisp
# # print(shared_var)
# diff_prop = stats.norm(0, np.sqrt(shared_var))
# diff_in_sample_prop = (sector_10k.loc[2, "Cases_Total"] - sector_10k.loc[7, "Cases_Total"])  / total_Hisp
# p_val = 1 - diff_prop.cdf(diff_in_sample_prop)
# # print(shared_freq)
# # print(total_Hisp)
# print(p_val)



def find_p(industry1, industry2):
    all_industries_cases = sector_10k["Cases_Total"].sum(axis = 0)
    shared_freq = (sector_10k.loc[industry1, "Cases_Total"] + sector_10k.loc[industry2, "Cases_Total"]) / all_industries_cases
    shared_var = (2 * (shared_freq) * (1 - shared_freq))/ all_industries_cases
    diff_prop = stats.norm(0, np.sqrt(shared_var))
    diff_in_sample_prop = (sector_10k.loc[industry1, "Cases_Total"] - sector_10k.loc[industry2, "Cases_Total"]) / all_industries_cases
    p_val = 1 - diff_prop.cdf(diff_in_sample_prop)  
    return p_val
#print(find_p('Manufacturing', 'Food Service'))

array_pval = np.empty((8, 8))
for industry, i in zip(sector_10k.index, range(8)):
    for other_industry, j in zip(sector_10k.index, range(8)):
        array_pval[i, j] = find_p(industry, other_industry)

#print(array_pval[array_pval < .05])
fig, ax = plt.subplots()
ax = sns.heatmap(np.array(array_pval), xticklabels = sector_10k.index, yticklabels = sector_10k.index)
plt.show()

        

